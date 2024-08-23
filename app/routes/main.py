import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import Integer, cast
from app.models import Item
from app.utils import parse_xml, fuzzy_search
from app import db


bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return redirect(url_for('main.search'))

@bp.route('/import', methods=['GET', 'POST'])
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
    
    if not re.match(r'^RPDC.*(B|C).*\.xml$', file.filename, re.IGNORECASE):
        flash('Formato inválido, insira um arquivo de relatório de compra de itens ou relatório de compra de no formato paisagem no formato XML')
        return redirect(request.url)
    
    xml_data = file.read()
    success_count, update_count = parse_xml(xml_data)
    flash(f'{success_count} entries added and {update_count} entries updated successfully!')
    
    return redirect(url_for('main.home'), code=302)

@bp.route('/item/<int:item_id>')
@login_required
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)



@bp.route('/search', methods=['GET', 'POST'])
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
                items = Item.query.order_by(cast(Item.cod_pedc, Integer).desc()).all()
                results = fuzzy_search(query, items)
            else:
                if filters == []:
                   query = ""
                results = Item.query.filter(db.or_(*filters)).order_by(cast(Item.cod_pedc, Integer).desc()).all()
                           
        else:
            results = Item.query.order_by(cast(Item.cod_pedc, Integer).desc()).limit(100).all()
    else:
        results = Item.query.order_by(cast(Item.cod_pedc, Integer).desc()).limit(100).all()
        
    last_updated_item = Item.query.order_by(cast(Item.cod_pedc, Integer).desc()).first()
    last_update_date = last_updated_item.dt_emis if last_updated_item else "No updates"

    return render_template('search.html', items=results, query=query, misspelling=misspelling, filter_by=filter_by, last_update_date=last_update_date)


