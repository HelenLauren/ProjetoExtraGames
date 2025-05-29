const form = document.getElementById('form-user');
const nomeInput = document.getElementById('nome');
const emailInput = document.getElementById('email');
const tabela = document.getElementById('tabela-usuarios').querySelector('tbody');

let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
let editIndex = null;

function salvarDados() {
  localStorage.setItem('usuarios', JSON.stringify(usuarios));

function renderizarTabela() {
  tabela.innerHTML = '';
  usuarios.forEach(user, index) => {
    const tr = document.createElement('tr');

    tr.innerHTML = `
      <td>${user.nome}</td>
      <td>${user.nome}</td>
      <td>
          <button onclick="editarUsuario(${index})">Editar</button>
          <button onclick="deletarUsuario(${index})">Excluir</button>
      </td>
    `;

     tabela.appendChild(tr);
   });
}

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const nome = nomeInput.value;
  const email = emailInput.value;

  if (editIndex === null) {
    usuarios.push({nome, email});
  } else {
    usuarios[editIndex] = {nome, email};
    editIndex = null;
  }

  salvarDados();
  renderizarTabela();
  form.reset();
});

function editarUsuario(index) {
  const user = usuarios[index];
  nomeInput.value = user.nome;
  emailInput.value = user.email;
  editIndex = index;
}

function deletarUsuario(index) {
  usuarios.splice(index, 1);
  salvarDados();
  renderizarTabela();
}

renderizarTabela();
