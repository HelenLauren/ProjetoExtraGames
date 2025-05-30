CREATE DATABASE crud_python;

USE crud_python;

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE perfis (
  id INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(100) NOT NULL
);

CREATE TABLE usuario_perfil (
  usuario_id INT,
  perfil_id INT,
  PRIMARY KEY (usuario_id, perfil_id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (perfil_id) REFERENCES perfis(id)
);


-- PT 2

CREATE USER 'crud_python'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
GRANT ALL ON crud_python.* to 'crud_python'@'localhost';
flush privileges;

INSERT INTO perfis (id, descricao)
VALUES (1, 'Administrador');

INSERT INTO usuarios (id, nome, email)
VALUES (1, 'Admin', 'admin@admin.com');
  
INSERT INTO usuario_perfil (usuario_id, perfil_id)
VALUES (1, 1);

INSERT INTO perfis (id, descricao)
VALUES (2, 'Leitor');

INSERT INTO usuarios (id, nome, email)
VALUES (2, 'User', 'usuario@gmail.com');

INSERT INTO usuario_perfil (usuario_id, perfil_id)
VALUES (2, 2);
