document.addEventListener('DOMContentLoaded', () => {
    // Modal Logic
    const modal = document.getElementById("manageModal");
    const btn = document.getElementById("btnManage");
    const span = document.getElementsByClassName("close")[0];
    const tabs = document.querySelectorAll(".tab-btn");
    
    if (btn) btn.onclick = () => {
        modal.style.display = "block";
        loadDrivers();
        loadFreights();
        loadRegions();
        loadFreightTypes();
    };
    
    if (span) span.onclick = () => modal.style.display = "none";
    
    window.onclick = (event) => {
        if (event.target == modal) modal.style.display = "none";
    };

    // Tabs
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            
            tab.classList.add("active");
            document.getElementById(tab.dataset.tab + "Tab").classList.add("active");
        });
    });

    // Drivers
    const driversList = document.getElementById("driversList");
    const addDriverForm = document.getElementById("addDriverForm");

    async function loadDrivers() {
        try {
            const res = await fetch('/api/drivers');
            if (!res.ok) throw new Error("Failed to fetch drivers");
            const drivers = await res.json();
            driversList.innerHTML = drivers.map(d => `
                <div class="data-item">
                    <span>${d.id} - ${d.name}</span>
                    <span class="delete-btn" onclick="window.deleteDriver(${d.id})">X</span>
                </div>
            `).join('');

            const driverSelect = document.getElementById("driverSelect");
            if (driverSelect) {
                driverSelect.innerHTML = '<option value="">Selecione...</option>' + 
                    drivers.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
            }
        } catch (err) {
            console.error(err);
        }
    }
    
    window.deleteDriver = async (id) => {
        if(!confirm("Deletar motorista?")) return;
        try {
            await fetch(`/api/drivers/${id}`, { method: 'DELETE' });
            loadDrivers();
        } catch (err) {
            console.error(err);
        }
    };

    if (addDriverForm) {
        addDriverForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(addDriverForm);
            const data = Object.fromEntries(formData.entries());
            
            try {
                await fetch('/api/drivers', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                addDriverForm.reset();
                loadDrivers();
            } catch (err) {
                console.error(err);
            }
        };
    }

    // Freights
    const freightsList = document.getElementById("freightsList");
    const addFreightForm = document.getElementById("addFreightForm");

    async function loadFreights() {
        try {
            const res = await fetch('/api/freights');
             if (!res.ok) throw new Error("Failed to fetch freights");
            const freights = await res.json();
            freightsList.innerHTML = freights.map(f => `
                <div class="data-item">
                    <span>#${f.id} - R$ ${f.value} (${f.expected_delivery_date})</span>
                    <span class="delete-btn" onclick="window.deleteFreight(${f.id})">X</span>
                </div>
            `).join('');
        } catch (err) {
            console.error(err);
        }
    }

    window.deleteFreight = async (id) => {
        if(!confirm("Deletar frete?")) return;
        try {
            await fetch(`/api/freights/${id}`, { method: 'DELETE' });
            loadFreights();
        } catch (err) {
            console.error(err);
        }
    };

    if (addFreightForm) {
        addFreightForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(addFreightForm);
            const data = Object.fromEntries(formData.entries());
            
            try {
                await fetch('/api/freights', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                addFreightForm.reset();
                loadFreights();
            } catch (err) {
                console.error(err);
            }
        };
    }

    const regionSelect = document.getElementById("regionSelect");

    async function loadRegions() {
        if (!regionSelect) return;
        try {
            const res = await fetch('/api/regions');
            if (!res.ok) throw new Error("Failed to fetch regions");
            const regions = await res.json();
            
            // Keep the first option (Selecione...)
            regionSelect.innerHTML = '<option value="">Selecione...</option>' + 
                regions.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
        } catch (err) {
            console.error(err);
        }
    }

    async function loadFreightTypes() {
        const freightTypeSelect = document.getElementById("freightTypeSelect");
        if (!freightTypeSelect) return;
        try {
            const res = await fetch('/api/freight_types');
            if (!res.ok) throw new Error("Failed to fetch freight types");
            const types = await res.json();
            
            freightTypeSelect.innerHTML = '<option value="">Selecione...</option>' + 
                types.map(t => `<option value="${t.id}">${t.description}</option>`).join('');
        } catch (err) {
            console.error(err);
        }
    }
});
