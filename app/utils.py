import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
from .models import Item
from . import db

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

    # Parse the XML data for `G_ITEM` entries (for the `RPDC0250B.xml` format)
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

    # Parse the XML data for `CGG_TPEDC_ITEM` entries (for the `RPDC0250C.xml` format)
    for cgg_item in root.findall('.//CGG_TPEDC_ITEM'):
        cod_pedc = cgg_item.find('CODIGO_PEDIDO').text

        existing_item = Item.query.filter_by(cod_pedc=cod_pedc).first()

        if existing_item:
            existing_item.qtde_atendida = cgg_item.find('QTDE_ATENDIDA').text
            existing_item.unid_med = cgg_item.find('UNID_MED').text
            num_nfs = []
            for g_nfe in cgg_item.findall('.//G_NFE'):
                num_nf = g_nfe.find('NUM_NF').text
                if num_nf:
                    num_nfs.append(num_nf)
            existing_item.num_nf = num_nfs  # Assuming `num_nf` is stored as a list in the model
            count_updates += 1

    db.session.commit()
    
    return count_success, count_updates
