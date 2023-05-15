/*
 * Máscaras disponíveis
 * Telefone: mask-telefone
 * Data: mask-data
 * CEP: mask-cep
 * CPF: mask-cpf
 * CNPJ: mask-cnpj
 * CPF e CNPJ no mesmo campo: mask-cpf-cnpj
 * Valor/Moeda: mask-valor
 * Credor SIAF: mask-siaf
 */

// /* 
var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
    spOptions = {
        onKeyPress: function (val, e, field, options) {
            field.mask(SPMaskBehavior.apply({}, arguments), options);
        }
    };

var options = {
    onKeyPress: function (cpf, ev, el, op) {
        var masks = ['000.000.000-000', '00.000.000/0000-00'];
        django.jQuery('.mask-cpf-cnpj').mask((cpf.length > 14) ? masks[1] : masks[0], op);
    }
}

django.jQuery(function () {
    django.jQuery('.mask-telefone').mask(SPMaskBehavior, spOptions);
    django.jQuery('.mask-mes-ano').mask('00/0000');
    django.jQuery('.mask-data').mask('00/00/0000');
    django.jQuery('.mask-cep').mask('00000-000');
    django.jQuery('.mask-cpf').mask('000.000.000-00', { reverse: true });
    django.jQuery('.mask-cnpj').mask('00.000.000/0000-00', { reverse: true });
    django.jQuery('.mask-cpf-cnpj').length > 11 ? django.jQuery('.mask-cpf-cnpj').mask('00.000.000/0000-00', options) : django.jQuery('.mask-cpf-cnpj').mask('000.000.000-00#', options);
    django.jQuery('.mask-money').mask('0.000.000.000,00', {reverse: true});
    django.jQuery('.mask-siaf').mask('000000');

    django.jQuery('form').submit(function () {
        var id_form = django.jQuery(this).attr('id');

        django.jQuery('#' + id_form).find(":input[class*='mask-cpf']").unmask();
        django.jQuery('#' + id_form).find(":input[class*='mask-cnpj']").unmask();
    });

    django.jQuery('.numero').keypress(function (event) {
        var tecla = (window.event) ? event.keyCode : event.which;
        if ((tecla > 47 && tecla < 58 || tecla == 45 || tecla == 13)) {
            return true;
        } else {
            if (tecla != 8) {
                return false;
            } else {
                return true;
            }

        }
    });

    django.jQuery(".maiusculo").keyup(function () {
        django.jQuery(this).val(django.jQuery(this).val().toUpperCase());
    });

    django.jQuery(".minusculo").keyup(function () {
        django.jQuery(this).val(django.jQuery(this).val().toLowerCase());
    });
});

function ocultarLinks(campo, acoes) {
    for (var i = 0; i < acoes.length; i++) {
        if (acoes[i] == 'desativa_campo') {
            var descricao = django.jQuery('#id_' + campo + ' option:selected').text();
            
            django.jQuery('.field-' + campo + ' .related-widget-wrapper').hide();
            django.jQuery('.field-' + campo + ' div:first-child').after('<span id="id_' + campo + '_conteudo"></span>');
            django.jQuery('#id_' + campo + '_conteudo').html(descricao);
        } else {
            django.jQuery('#' + acoes[i] + '_id_' + campo).remove();
            // django.jQuery('#' + acoes[i] + '_id_' + campo).hide();
        }
    }
}
// */
/*
var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
    spOptions = {
        onKeyPress: function (val, e, field, options) {
            field.mask(SPMaskBehavior.apply({}, arguments), options);
        }
    };

var options = {
    onKeyPress: function (cpf, ev, el, op) {
        var masks = ['000.000.000-000', '00.000.000/0000-00'];
        $('.mask-cpf-cnpj').mask((cpf.length > 14) ? masks[1] : masks[0], op);
    }
}

$(document).ready(function(){
    $('.mask-telefone').mask(SPMaskBehavior, spOptions);
    $('.mask-data').mask('00/00/0000');
    $('.mask-cep').mask('00000-000');
    $('.mask-cpf').mask('000.000.000-00', { reverse: true });
    $('.mask-cnpj').mask('00.000.000/0000-00', { reverse: true });
    $('.mask-cpf-cnpj').length > 11 ? $('.mask-cpf-cnpj').mask('00.000.000/0000-00', options) : $('.mask-cpf-cnpj').mask('000.000.000-00#', options);
    $('.mask-valor').maskMoney({ showSymbol: false, symbol: "", precision: 2, decimal: ",", thousands: "." });

    // Limpa as mascaras antes de salvar valor
    $('form').submit(function () {
        var id_form = $(this).attr('id');

        $('#' + id_form).find(":input[class*='mask-']").unmask();
    });

    $('.numero').keypress(function (event) {
        var tecla = (window.event) ? event.keyCode : event.which;
        if ((tecla > 47 && tecla < 58 || tecla == 45 || tecla == 13)) {
            return true;
        } else {
            if (tecla != 8) {
                return false;
            } else {
                return true;
            }

        }
    });

    $(".maiusculo").keyup(function () {
        $(this).val($(this).val().toUpperCase());
    });

    $(".minusculo").keyup(function () {
        $(this).val($(this).val().toLowerCase());
    });
});
// */