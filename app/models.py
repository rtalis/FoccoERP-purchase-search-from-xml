from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    num_nf = db.Column(db.PickleType, nullable=True)  # Storing list of NUM_NF
    qtde_atendida = db.Column(db.String(50), nullable=True)
    unid_med = db.Column(db.String(50), nullable=True)
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
            'num_nf': self.num_nf,
            'qtde_atendida': self.qtde_atendida,
            'unid_med': self.unid_med
           # 'comprador': self.comprador,
           # 'insert_by': self.insert_by
            
        }
    def __repr__(self):
        return f'<Item {self.cod_pedc}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
