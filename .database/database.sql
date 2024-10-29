-- Apaga o banco de dados.
-- PERIGO! Só use isso em modo de desenvolvimento.
DROP DATABASE IF EXISTS crudtrecos;

-- Cria o banco de dados "novamente".
-- PERIGO! Só use isso em modo de desenvolvimento.
CREATE DATABASE crudtrecos
    -- Seleciona a tabela de caracteres UTF-8 (acentuação).
    CHARACTER SET utf8mb4
    -- Permite buscas case-insensitive (A=a, ç=c, ã=a).
    COLLATE utf8mb4_unicode_ci;

-- Seleciona o banco de dados
-- Todos comandos seguintes sejam para este banco de dados
USE crudtrecos;

-- Cria a tabela da entidade "usuario"
-- Prefixo dos atributos → u_
CREATE TABLE usuario (
    u_id INT PRIMARY KEY AUTO_INCREMENT,
    u_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    u_nome VARCHAR(127) NOT NULL,
    u_nascimento DATE NOT NULL,
    u_email VARCHAR(255) NOT NULL,
    u_senha VARCHAR(63) NOT NULL,
    u_status ENUM ('on', 'off', 'del') DEFAULT 'on'
);

-- Cria a tabela da entidade "treco"
-- Prefixo dos atributos → t_
CREATE TABLE treco (
    t_id INT PRIMARY KEY AUTO_INCREMENT,
    t_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    t_foto VARCHAR(255),
    t_usuario INT NOT NULL,
    t_nome VARCHAR(127) NOT NULL,
    t_descricao TEXT,
    t_localizacao VARCHAR(255),
    t_status ENUM ('on', 'off', 'del') DEFAULT 'on',
    FOREIGN KEY (t_usuario) REFERENCES usuario(u_id)
);