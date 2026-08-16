const planNormal = document.getElementById('plan_normal');
const planEspecial = document.getElementById('plan_especial');
const campoMonto = document.getElementById('monto');

planNormal.addEventListener('change', function(){
    campoMonto.value = 180;
    campoMonto.disabled = true;
    campoMonto.required = false;
})

planEspecial.addEventListener('change',function(){
    campoMonto.value = '';
    campoMonto.disabled = false;
    campoMonto.required = true;
})