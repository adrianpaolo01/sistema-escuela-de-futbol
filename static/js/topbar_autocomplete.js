// Topbar autocomplete: fetch alumnos list from server and provide suggestions
(async function(){
    const input = document.querySelector('.topbar-search .search');
    if(!input) return;

    // Create dropdown
    const container = document.createElement('div');
    container.className = 'topbar-autocomplete';
    container.style.position = 'absolute';
    container.style.background = '#fff';
    container.style.boxShadow = '0 6px 18px rgba(0,0,0,0.08)';
    container.style.borderRadius = '8px';
    container.style.width = 'min(520px, 100%)';
    container.style.maxHeight = '240px';
    container.style.overflow = 'auto';
    container.style.zIndex = '60';
    container.style.display = 'none';

    input.parentElement.style.position = 'relative';
    input.parentElement.appendChild(container);

    // Load alumnos
    let alumnos = [];
    try{
        const res = await fetch('/api/alumnos_json');
        if(res.ok) alumnos = await res.json();
    }catch(e){ console.warn('No se pudo cargar lista de alumnos', e); }

    input.addEventListener('input', function(){
        const q = input.value.trim().toLowerCase();
        container.innerHTML = '';
        if(!q){ container.style.display = 'none'; return; }

        const filtrados = alumnos.filter(a => a.nombre.toLowerCase().includes(q)).slice(0,20);
        filtrados.forEach(a => {
            const it = document.createElement('div');
            it.textContent = a.nombre;
            it.style.padding = '8px 12px';
            it.style.cursor = 'pointer';
            it.addEventListener('mouseenter', ()=> it.style.background = '#f4f6f8');
            it.addEventListener('mouseleave', ()=> it.style.background = '');
            it.addEventListener('click', ()=>{
                input.value = a.nombre;
                container.style.display = 'none';
                // Optionally submit the form
                // input.closest('form').submit();
            });
            container.appendChild(it);
        });

        container.style.display = filtrados.length ? 'block' : 'none';
    });

    document.addEventListener('click', function(e){
        if(!input.parentElement.contains(e.target)) container.style.display = 'none';
    });
})();
