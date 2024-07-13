from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
from fuzzywuzzy import fuzz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

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

    def __repr__(self):
        return f'<Item {self.cod_pedc}>'

with app.app_context():
    db.create_all()

def fuzzy_search(query, items):
    results = []
    for item in items:
        ratio = fuzz.partial_ratio(query.lower(), item.descricao.lower())
        if ratio >= 70:  # Adjust the threshold as needed
            results.append(item)
    return results

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    count_success = 0  # Counter for successful imports

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

        existing_item = Item.query.filter_by(cod_pedc=item_data['cod_pedc'], empr_id=item_data['empr_id'], descricao_item=item_data['descricao_item']).first()
        if not existing_item:
            new_item = Item(**item_data)
            db.session.add(new_item)
            count_success += 1  # Increment the count for each successfully added item
    
    db.session.commit()
    return count_success  # Return the count of successful imports

@app.route('/')
def home():
    return redirect(url_for('search'))

@app.route('/import', methods=['GET', 'POST'])
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
    success_count = parse_xml(xml_data)  # Get the count of successful imports
    flash(f'{success_count} entries imported successfully')
    
    return redirect(url_for('home'), code=302)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = ''
    misspelling = False
    filter_by = ['cod_pedc', 'descricao', 'cod_item', 'id_item_ped']

    if request.method == 'POST':
        query = request.form.get('query', '')
        misspelling = request.form.get('misspelling') == 'on'
        filter_by = request.form.getlist('filter_by')

        if query != "":
            filters = []
            if 'cod_pedc' in filter_by:
                filters.append(Item.cod_pedc.contains(query))
            if 'descricao' in filter_by:
                filters.append(Item.descricao.contains(query))
            if 'cod_item' in filter_by:
                filters.append(Item.cod_item.contains(query))
            if 'id_item_ped' in filter_by:
                filters.append(Item.id_item_ped.contains(query))
            
            if misspelling:
                items = Item.query.order_by(Item.cod_pedc.desc()).all()
                results = fuzzy_search(query, items)
            else:
                results = Item.query.filter(db.or_(*filters)).order_by(Item.cod_pedc.desc()).all()
        else:
            results = Item.query.order_by(Item.cod_pedc.desc()).all()
    else:
        results = Item.query.order_by(Item.cod_pedc.desc()).all()
   
    return render_template('search.html', items=results, query=query, misspelling=misspelling, filter_by=filter_by)




if __name__ == '__main__':
    app.run(debug=True)
