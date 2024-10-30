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

-- -------------------------------------- --
-- Insere alguns dados "fake" nas tabelas --
-- -------------------------------------- --

-- Tabela 'usuario'
INSERT INTO usuario (
    u_nome,
    u_nascimento,
    u_email,
    u_senha
) VALUES (
    'Joca da Silva',
    '2000-04-25',
    'jocasilva@email.com',
    SHA1('Senha123') -- Criptografa a senha do usuário
), (
    'Marineuza Siriliano',
    '2003-03-12',
    'marineuza@email.com',
    SHA1('Senha123')
), (
    'Setembrino Trocatapas',
    '1998-12-14',
    'setbrino@email.com',
    SHA1('Senha123')
);

-- Tabela 'treco'
INSERT INTO treco (
    t_foto,
    t_usuario,
    t_nome,
    t_descricao,
    t_localizacao
) VALUES ( 
    'https://picsum.photos/200', 
    '1', -- Id de um usuário existente
    'Caneca de café do Elon Musk', 
    'Uma caneca feia pra caracas que arrumei em algum lugar.', 
    'Na estante da sala, prateleira de baixo.'
), (
    'https://picsum.photos/199',
    '1',
    'Caneca do Curintia',
    'Cabem 300 ml, mas está com a alça quebrada e colada com superbondi.',
    'Na estante da sala, prateleira do meio.'
);

-- Inserções da IA (veja o prompt no material da aula 11)
INSERT INTO treco (t_foto, t_usuario, t_nome, t_descricao, t_localizacao) VALUES
    ('https://picsum.photos/201', '1', 'Livro de Física Quântica', 'Um livro velho e empoeirado que encontrei na feira.', 'Na mesa do escritório, ao lado do laptop.'),
    ('https://picsum.photos/202', '2', 'Câmera Polaroid', 'Uma câmera antiga, mas ainda funcional.', 'Na prateleira do quarto, junto às fotos antigas.'),
    ('https://picsum.photos/203', '1', 'Relógio de Parede Vintage', 'Relógio com design clássico, não funciona mais.', 'Na parede da cozinha, ao lado do armário.'),
    ('https://picsum.photos/204', '2', 'Guitarra Elétrica', 'Guitarra sem uma corda, mas ainda toca bem.', 'No canto da sala, perto do amplificador.'),
    ('https://picsum.photos/205', '1', 'Bolsa de Couro', 'Bolsa de couro marrom, um pouco desgastada.', 'No guarda-roupa, pendurada ao lado dos casacos.'),
    ('https://picsum.photos/206', '2', 'Vinil dos Beatles', 'Disco de vinil, edição original dos anos 60.', 'Na prateleira da sala, junto aos outros discos.'),
    ('https://picsum.photos/207', '1', 'Óculos de Sol Ray-Ban', 'Óculos com uma lente riscada.', 'Na gaveta do armário, junto aos acessórios.'),
    ('https://picsum.photos/208', '2', 'Estátua de Buda', 'Pequena estátua de Buda de madeira.', 'No altar da sala, cercada de velas.'),
    ('https://picsum.photos/209', '1', 'Bola de Futebol Autografada', 'Bola autografada por um jogador famoso.', 'Na estante da sala, prateleira de cima.'),
    ('https://picsum.photos/210', '2', 'Computador Retro', 'Computador antigo dos anos 80, ainda funcionando.', 'No escritório, em cima da mesa antiga.');
