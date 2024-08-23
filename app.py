from flask import Flask, request, render_template, redirect, url_for, flash,  jsonify
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
from playwright.sync_api import sync_playwright, expect
from fuzzywuzzy import fuzz
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user,UserMixin
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.update(
    SESSION_COOKIE_SECURE=True,
    REMEMBER_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True
)





class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_entrega = db.Column(db.String(10))
    id_item_ped = db.Column(db.String(50))
    masc_item_id = db.Column(db.String(50))
    ites_id = db.Column(db.String(50))
    empr_id = db.Column(db.String(50))
    itempr_id = db.Column(db.String(50))
    descricao_item = db.Column(db.String(200))
    cod_item = db.Column(db.String(50))
    descricao = db.Column(db.String(200))
    cod_pedc = db.Column(db.String(50))
    dt_emis = db.Column(db.String(10))
    moeped_id = db.Column(db.String(50))
    qtde_pedida = db.Column(db.String(50))
    qtde_entregue = db.Column(db.String(50))
    qtde_canc = db.Column(db.String(50))
    cod_grp_ite = db.Column(db.String(50))
    cod_for = db.Column(db.String(50))
    tot_bruto = db.Column(db.String(50))
    vlr_entregue = db.Column(db.String(50))
    tfd_i_id = db.Column(db.String(50))
    cf_converte_moeda = db.Column(db.String(50))
    cp_vlr_entregue = db.Column(db.String(50))
    cp_tot_bruto = db.Column(db.String(50))
    cf_vlr_saldo = db.Column(db.String(50))
    cf_qtde_saldo = db.Column(db.String(50))
    cs_tot_bruto = db.Column(db.String(50))
    cs_valor_entregue = db.Column(db.String(50))
    cf_retorna_mascara = db.Column(db.String(50))
    cs_conta_desenhos = db.Column(db.String(50))
    cs_conta_pedidos = db.Column(db.String(50))
    cf_retorna_codigo = db.Column(db.String(50))
    #comprador = db.Column(db.String(200))
    #insert_by = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'dt_entrega': self.dt_entrega,
            'id_item_ped': self.id_item_ped,
            'masc_item_id': self.masc_item_id,
            'ites_id': self.ites_id,
            'empr_id': self.empr_id,
            'itempr_id': self.itempr_id,
            'descricao_item': self.descricao_item,
            'cod_item': self.cod_item,
            'descricao': self.descricao,
            'cod_pedc': self.cod_pedc,
            'dt_emis': self.dt_emis,
            'moeped_id': self.moeped_id,
            'qtde_pedida': self.qtde_pedida,
            'qtde_entregue': self.qtde_entregue,
            'qtde_canc': self.qtde_canc,
            'cod_grp_ite': self.cod_grp_ite,
            'cod_for': self.cod_for,
            'tot_bruto': self.tot_bruto,
            'vlr_entregue': self.vlr_entregue,
            'tfd_i_id': self.tfd_i_id,
            'cf_converte_moeda': self.cf_converte_moeda,
            'cp_vlr_entregue': self.cp_vlr_entregue,
            'cp_tot_bruto': self.cp_tot_bruto,
            'cf_vlr_saldo': self.cf_vlr_saldo,
            'cf_qtde_saldo': self.cf_qtde_saldo,
            'cs_tot_bruto': self.cs_tot_bruto,
            'cs_valor_entregue': self.cs_valor_entregue,
            'cf_retorna_mascara': self.cf_retorna_mascara,
            'cs_conta_desenhos': self.cs_conta_desenhos,
            'cs_conta_pedidos': self.cs_conta_pedidos,
            'cf_retorna_codigo': self.cf_retorna_codigo,
           # 'comprador': self.comprador,
           # 'insert_by': self.insert_by
        }
    def __repr__(self):
        return f'<Item {self.cod_pedc}>'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')




@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('search'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))







def fuzzy_search(query, items):
    results = []
    for item in items:
        ratio = fuzz.partial_ratio(query.lower(), item.descricao_item.lower())
        if ratio >= 70:  # Adjust the threshold as needed
            results.append(item)
        else:
            ratio = fuzz.partial_ratio(query.lower(), item.descricao.lower())
            if ratio >= 70:  # Adjust the threshold as needed
                results.append(item)
    return results

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    count_success = 0 
    count_updates = 0
    # Counter for successful imports

    for g_item in root.findall('.//G__ITEM'):
        item_data = {
            'dt_entrega': g_item.find('DT_ENTREGA').text,
            'id_item_ped': g_item.find('ID_ITEM_PED').text,
            'masc_item_id': g_item.find('MASC_ITEM_ID').text or '',
            'ites_id': g_item.find('ITES_ID').text,
            'empr_id': g_item.find('EMPR_ID').text,
            'itempr_id': g_item.find('ITEMPR_ID').text,
            'descricao_item': g_item.find('DESCRICAO_ITEM').text,
            'cod_item': g_item.find('COD_ITEM').text,
            'descricao': g_item.find('DESCRICAO').text,
            'cod_pedc': g_item.find('COD_PEDC').text,
            'dt_emis': g_item.find('DT_EMIS').text,
            'moeped_id': g_item.find('MOEPED_ID').text or '',
            'qtde_pedida': g_item.find('QTDE_PEDIDA').text,
            'qtde_entregue': g_item.find('QTDE_ENTREGUE').text,
            'qtde_canc': g_item.find('QTDE_CANC').text,
            'cod_grp_ite': g_item.find('COD_GRP_ITE').text,
            'cod_for': g_item.find('COD_FOR').text,
            'tot_bruto': g_item.find('TOT_BRUTO').text,
            'vlr_entregue': g_item.find('VLR_ENTREGUE').text,
            'tfd_i_id': g_item.find('TFD_I_ID').text,
            'cf_converte_moeda': g_item.find('CF_CONVERTE_MOEDA').text,
            'cp_vlr_entregue': g_item.find('CP_VLR_ENTREGUE').text,
            'cp_tot_bruto': g_item.find('CP_TOT_BRUTO').text,
            'cf_vlr_saldo': g_item.find('CF_VLR_SALDO').text,
            'cf_qtde_saldo': g_item.find('CF_QTDE_SALDO').text,
            'cs_tot_bruto': g_item.find('CS_TOT_BRUTO').text,
            'cs_valor_entregue': g_item.find('CS_VALOR_ENTREGUE').text,
            'cf_retorna_mascara': g_item.find('CF_RETORNA_MASCARA').text,
            'cs_conta_desenhos': g_item.find('CS_CONTA_DESENHOS').text,
            'cs_conta_pedidos': g_item.find('CS_CONTA_PEDIDOS').text,
            'cf_retorna_codigo': g_item.find('CF_RETORNA_CODIGO').text
            
        }

        existing_item = Item.query.filter_by(
            cod_pedc=item_data['cod_pedc'], 
            empr_id=item_data['empr_id'], 
            descricao_item=item_data['descricao_item']
        ).first()
        
        if existing_item:
            for key, value in item_data.items():
                setattr(existing_item, key, value)
            count_updates += 1
        else:
            new_item = Item(**item_data)
            db.session.add(new_item)
            count_success += 1

    db.session.commit()
    
    return count_success, count_updates

@app.route('/')
def home():
    return redirect(url_for('search'))

@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.ico')

@app.route('/import', methods=['GET', 'POST'])
@login_required
def import_data():
    if request.method == 'GET':
        return render_template('import.html')
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # Check if the filename matches the required pattern
    filename = file.filename
    if not re.match(r'^RPDC.*B.*\.xml$', filename, re.IGNORECASE):
        flash('Formato inválido. Insira um relatório de pedidos de compra do FOCCO layout LISTAGEM DE ITENS em formato XML')
        return redirect(request.url)
    
    # Proceed with handling the valid XML file
    xml_data = file.read()
    success_count, update_count = parse_xml(xml_data)  # Get the count of successful imports
    flash(f'{success_count} entradas adicionadas e {update_count} entradas atualizadas com sucesso!')
    
    return redirect(url_for('home'), code=302)

@app.route('/item/<int:item_id>')
@login_required
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query = ''
    misspelling = False
    filter_by = ['cod_pedc', 'descricao', 'cod_item', 'descricao_item']

    if request.method == 'POST':
        query = request.form.get('query', '')
        misspelling = request.form.get('misspelling') == 'on'
        filter_by = request.form.getlist('filter_by')

        if query != "":
            filters = []
            if 'descricao_item' in filter_by:
                filters.append(Item.descricao_item.contains(query))
            if 'cod_pedc' in filter_by:
                filters.append(Item.cod_pedc.contains(query))
            if 'descricao' in filter_by:
                filters.append(Item.descricao.contains(query))
            if 'cod_item' in filter_by:
                filters.append(Item.cod_item.contains(query))
            
            if misspelling:
                items = Item.query.order_by(Item.cod_pedc.desc()).all()
                results = fuzzy_search(query, items)
            else:
                if filters == []:
                   query = ""
                results = Item.query.filter(db.or_(*filters)).order_by(Item.cod_pedc.desc()).all()
                                
            
        else:
            results = Item.query.order_by(Item.cod_pedc.desc()).limit(100).all()
    else:
        results = Item.query.order_by(Item.cod_pedc.desc()).limit(100).all()
        
    last_updated_item = Item.query.order_by(Item.cod_pedc.desc()).first()
    last_update_date = last_updated_item.dt_emis if last_updated_item else "No updates"

    return render_template('search.html', items=results, query=query, misspelling=misspelling, filter_by=filter_by, last_update_date=last_update_date)





if __name__ == '__main__':
    app.run(debug=True)
