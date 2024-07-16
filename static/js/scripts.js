document.addEventListener('DOMContentLoaded', function() {
    console.log("loaded")
    var modal = document.getElementById('item-modal');
    var span = document.getElementsByClassName('close')[0];
    var itemDetails = document.getElementById('item-details');

    document.querySelectorAll('.item-row').forEach(function(row) {
        row.addEventListener('click', function() {
            console.log(this.dataset.item)
            var item = JSON.parse(this.dataset.item);
            console.log("clicked")
            console.log(item)
            var detailsHtml = `
                <strong>Data Entrega:</strong> ${item.dt_entrega}<br>
                <strong>ID Item Pedido:</strong> ${item.id_item_ped}<br>
                <strong>Máscara Item ID:</strong> ${item.masc_item_id}<br>
                <strong>ITES ID:</strong> ${item.ites_id}<br>
                <strong>EMPR ID:</strong> ${item.empr_id}<br>
                <strong>Item PR ID:</strong> ${item.itempr_id}<br>
                <strong>Descrição Item:</strong> ${item.descricao_item}<br>
                <strong>COD Item:</strong> ${item.cod_item}<br>
                <strong>Descrição:</strong> ${item.descricao}<br>
                <strong>COD PEDC:</strong> ${item.cod_pedc}<br>
                <strong>Data Emissão:</strong> ${item.dt_emis}<br>
                <strong>MOEPED ID:</strong> ${item.moeped_id}<br>
                <strong>Quantidade Pedida:</strong> ${item.qtde_pedida}<br>
                <strong>Quantidade Entregue:</strong> ${item.qtde_entregue}<br>
                <strong>Quantidade Cancelada:</strong> ${item.qtde_canc}<br>
                <strong>COD Grupo Item:</strong> ${item.cod_grp_ite}<br>
                <strong>COD Fornecedor:</strong> ${item.cod_for}<br>
                <strong>Total Bruto:</strong> R$ ${item.tot_bruto}<br>
                <strong>Valor Entregue:</strong> R$ ${item.vlr_entregue}<br>
                <strong>TFD I ID:</strong> ${item.tfd_i_id}<br>
                <strong>CF Converte Moeda:</strong> ${item.cf_converte_moeda}<br>
                <strong>CP Valor Entregue:</strong> R$ ${item.cp_vlr_entregue}<br>
                <strong>CP Total Bruto:</strong> R$ ${item.cp_tot_bruto}<br>
                <strong>CF Valor Saldo:</strong> R$ ${item.cf_vlr_saldo}<br>
                <strong>CF Quantidade Saldo:</strong> ${item.cf_qtde_saldo}<br>
                <strong>CS Total Bruto:</strong> R$ ${item.cs_tot_bruto}<br>
                <strong>CS Valor Entregue:</strong> R$ ${item.cs_valor_entregue}<br>
                <strong>CF Retorna Máscara:</strong> ${item.cf_retorna_mascara}<br>
                <strong>CS Conta Desenhos:</strong> ${item.cs_conta_desenhos}<br>
                <strong>CS Conta Pedidos:</strong> ${item.cs_conta_pedidos}<br>
                <strong>CF Retorna Código:</strong> ${item.cf_retorna_codigo}<br>
              
            `;
            itemDetails.innerHTML = detailsHtml;
            modal.style.display = 'block';
        });
    });
   // <strong>Comprador:</strong> ${item.comprador}<br>
    //<strong>Inserido por:</strong> ${item.insert_by}<br>
    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});

function runPlaywright(descricao, dt_entrega) {
    // Call Playwright script via a fetch request to your backend endpoint
    fetch('/run_playwright', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ descricao: descricao, dt_entrega: dt_entrega })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Playwright script executed successfully:', data);
        // Optionally handle success feedback to the user
    })
    .catch(error => {
        console.error('Error executing Playwright script:', error);
        // Handle error feedback to the user
    });
}
