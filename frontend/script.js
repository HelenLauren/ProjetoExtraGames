document.addEventListener('DOMContentLoaded', ()=> {
  const form = document.getElementById('form-user');
  const nomeInput = document.getElementById('nome');
  const emailInput = document.getElementById('email');
  const tabela = document.getElementById('tabela-usuarios').querySelector('tbody');
  let editId = null;

  async function carregarUsuarios() {
    try {
      const response = await fetch('http://localhost:5000/usuarios');
      if (!response.ok) throw new Error('Erro ao carregar usuários');
      const usuarios = await response.json();

      tabela.innerHTML = '';
      usuarios.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${user.nome}</td>
          <td>${user.email}</td>
          <td>${user.perfis || 'Sem perfil'}</td>
          <td>
            <button onclick="editarUsuario(${user.id}, '${user.nome}', '${user.email}')">Editar</button>
            <button onclick="deletarUsuario(${user.id})">Excluir</button>
          </td>
        `;
        tabela.appendChild(tr);
      });
    } catch (err) {
      console.error('Erro:', err);
      alert(err.message);
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    try{
      const method = editId ? 'PUT' : 'POST';
      const url = editId
        ? `http://localhost:5000/usuarios/${editId}`
        : 'http://localhost:5000/usuarios';

      const response = await fetch(url, {
        method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          nome: nomeInput.value,
          email: emailInput.value
        })
      });

      if (!response.ok) throw new Error('Erro ao salvar usuário');

      form.reset();
      editId = null;
      await carregarUsuarios();
    } catch (err) {
        console.error('Erro:', err);
        alert(err.message);
      }
  });

  window.editarUsuario = (id, nome, email) => {
    nomeInput.value = nome;
    emailInput.value = email;
    editId = id;
  };

  window.deletarUsuario = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return;

    try {
      const response = await fetch(`http://localhost:5000/usuarios/${id}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Erro ao deletar usuário');
      await carregarUsuarios();
    } catch (err) {
      console.error('Erro:', err);
      alert(err.message);
    }
  };

  carregarUsuarios();

});

