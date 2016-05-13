(function($) {
	$(document).ready(function() {
   /* Executa a requisiÃ§Ã£o quando o campo CEP perder o foco */
   $('#id_cep').blur(function(){
      var cep_code = $(this).val();
      if( cep_code.length <= 0 ) return;
      $.get("http://apps.widenet.com.br/busca-cep/api/cep.json", { code: cep_code },
         function(result){
            if( result.status!=1 ){
				document.getElementById('id_cep').value=""
				alert(result.message || "Houve um erro desconhecido");
				$('#id_cep').focus();
				return;
            }
			/*alert(result.code);*/
            $("input#id_cep").val( result.code );
            $("input#id_estado").val( result.state );
            $("input#id_cidade").val( result.city );
            $("input#id_bairro").val( result.district );
            $("input#id_rua").val( result.address );
			$('#id_numero_rua').focus();
			});
	  });
   });
})(django.jQuery);