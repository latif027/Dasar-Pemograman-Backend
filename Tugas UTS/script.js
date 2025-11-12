document.addEventListener("DOMContentLoaded", ()=>{
  loadCars();
  setupForm();
  setupModal();
});

function api(path, opts){ return fetch(path, opts).then(r=>{ if(!r.ok) throw r; return r.json(); }) }

function loadCars(){
  api('/api/mobil').then(data=>{
    const carList = document.getElementById('car-list');
    carList.innerHTML = '';
    data.forEach(car=>{
      const el = document.createElement('div'); el.className='card';
      el.innerHTML = `
        <img src="${car.gambar || 'https://via.placeholder.com/800x450?text=No+Image'}" alt="${car.nama}">
        <div class="card-body">
          <h3>${escapeHtml(car.nama)}</h3>
          <p>Rp ${Number(car.harga).toLocaleString()}</p>
          <div class="actions">
            <button class="btn primary" data-edit="${car.id}">Edit</button>
            <button class="btn danger" data-delete="${car.id}">Hapus</button>
          </div>
        </div>
      `;
      carList.appendChild(el);
    });
    // attach listeners
    document.querySelectorAll('[data-edit]').forEach(b=>b.addEventListener('click', onEditClick));
    document.querySelectorAll('[data-delete]').forEach(b=>b.addEventListener('click', onDeleteClick));
  }).catch(e=>{ console.error(e); document.getElementById('car-list').innerHTML='<p style="padding:20px">Gagal memuat data.</p>' })
}

function setupForm(){
  document.getElementById('addCarForm').addEventListener('submit', e=>{
    e.preventDefault();
    const nama = document.getElementById('nama').value.trim();
    const harga = Number(document.getElementById('harga').value);
    const gambar = document.getElementById('gambar').value.trim();
    api('/api/mobil', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({nama,harga,gambar})})
      .then(()=>{ loadCars(); e.target.reset(); })
      .catch(err=>{ alert('Gagal menambahkan mobil'); console.error(err); });
  });
}

/* Edit modal */
function setupModal(){
  const modal = document.getElementById('editModal');
  document.getElementById('closeModal').addEventListener('click', ()=> modal.classList.add('hidden'));
  document.getElementById('cancelEdit').addEventListener('click', ()=> modal.classList.add('hidden'));
  document.getElementById('editCarForm').addEventListener('submit', e=>{
    e.preventDefault();
    const id = Number(document.getElementById('editId').value);
    const nama = document.getElementById('editNama').value.trim();
    const harga = Number(document.getElementById('editHarga').value);
    const gambar = document.getElementById('editGambar').value.trim();
    api('/api/mobil/'+id, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({nama,harga,gambar})})
      .then(()=>{ loadCars(); document.getElementById('editModal').classList.add('hidden'); })
      .catch(err=>{ alert('Gagal menyimpan perubahan'); console.error(err); });
  });
}

function onEditClick(e){
  const id = e.currentTarget.getAttribute('data-edit');
  // fetch single
  api('/api/mobil/'+id).then(car=>{
    document.getElementById('editId').value = car.id;
    document.getElementById('editNama').value = car.nama;
    document.getElementById('editHarga').value = car.harga;
    document.getElementById('editGambar').value = car.gambar || '';
    document.getElementById('editModal').classList.remove('hidden');
  }).catch(()=>alert('Gagal mengambil data mobil'));
}

function onDeleteClick(e){
  const id = e.currentTarget.getAttribute('data-delete');
  if(!confirm('Hapus mobil ini?')) return;
  api('/api/mobil/'+id, {method:'DELETE'}).then(()=>loadCars()).catch(()=>alert('Gagal menghapus mobil'));
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, m=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m])) }
