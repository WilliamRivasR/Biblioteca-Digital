-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.9.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para biblioteca_escolar
CREATE DATABASE IF NOT EXISTS `biblioteca_escolar` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `biblioteca_escolar`;

-- Volcando estructura para procedimiento biblioteca_escolar.ActualizarUsuario
DELIMITER //
CREATE PROCEDURE `ActualizarUsuario`(
    IN doc INT,
    IN nombre VARCHAR(100),
    IN apellidos VARCHAR(100),
    IN fecha DATE,
    IN correo VARCHAR(100),
    IN telefono VARCHAR(20),
    IN contrasena VARCHAR(100)
)
BEGIN
    DECLARE usuario_existente INT;
    
    -- Verificar si el usuario existe
    SELECT COUNT(*)
    INTO usuario_existente
    FROM usuarios
    WHERE Numero_documento = doc;

    IF usuario_existente > 0 THEN
        -- Actualizar usuario si existe
        UPDATE usuarios
        SET Nombre = nombre,
            Apellidos = apellidos,
            Fecha_nacimiento = fecha,
            Correo_electronico = correo,
            Telefono = telefono,
            Contraseña = contrasena
        WHERE Numero_documento = doc;

        SELECT 'Usuario actualizado correctamente' AS mensaje;
    ELSE
        -- Mensaje si el usuario no existe
        SELECT 'Usuario no encontrado' AS mensaje;
    END IF;
END//
DELIMITER ;

-- Volcando estructura para procedimiento biblioteca_escolar.AgregarImagen
DELIMITER //
CREATE PROCEDURE `AgregarImagen`(
    IN p_image_name VARCHAR(255),
    IN p_image_path VARCHAR(255),
    OUT p_image_id INT
)
BEGIN
    INSERT INTO imagenes (nombre_imagen, ruta_imagen)
    VALUES (p_image_name, p_image_path);

    SET p_image_id = LAST_INSERT_ID();
END//
DELIMITER ;

-- Volcando estructura para procedimiento biblioteca_escolar.AgregarLibro
DELIMITER //
CREATE PROCEDURE `AgregarLibro`(
	IN `p_Titulo` VARCHAR(255),
	IN `p_Autor` VARCHAR(255),
	IN `p_Año_publicacion` INT,
	IN `p_Genero` VARCHAR(255),
	IN `p_Resumen` TEXT,
	IN `p_Ejemplares_disponibles` INT,
	IN `p_Estado` VARCHAR(50)
)
BEGIN
    DECLARE ID_libro INT;  -- Declarar la variable

    -- Insertar el nuevo libro en la tabla libros
    INSERT INTO libros (Titulo, Autor, Año_publicacion, Genero, Resumen, Ejemplares_disponibles, Estado)
    VALUES (p_Titulo, p_Autor, p_Año_publicacion, p_Genero, p_Resumen, p_Ejemplares_disponibles, p_Estado);

    -- Obtener el ID del libro recién insertado
    SET ID_libro = LAST_INSERT_ID();

    -- Verificar si se encontró el ID
    IF ID_libro IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se encontró el libro con el título proporcionado.';
    END IF;

    -- Devolver el ID del libro
    SELECT ID_libro AS ID_libro;

END//
DELIMITER ;

-- Volcando estructura para procedimiento biblioteca_escolar.AgregarLibroPrestado
DELIMITER //
CREATE PROCEDURE `AgregarLibroPrestado`(
	IN `numero_documento` VARCHAR(20),
	IN `libro_id` INT,
	IN `fecha_prestamo` DATE
)
BEGIN
    DECLARE libro_titulo VARCHAR(255);
    DECLARE usuario_existe INT;

    -- Obtener el título del libro con el ID proporcionado
    SELECT Titulo INTO libro_titulo
    FROM libros
    WHERE ID_libro = libro_id;

    -- Verificar si se obtuvo un título válido
    IF libro_titulo IS NOT NULL THEN
        -- Verificar si el usuario existe
        SELECT COUNT(*) INTO usuario_existe
        FROM usuarios
        WHERE Numero_documento = numero_documento;

        IF usuario_existe > 0 THEN
            -- Actualizar la columna Libros_prestados en la tabla de usuarios
            UPDATE usuarios
            SET Libros_prestados = CONCAT(IFNULL(Libros_prestados, ''), 
                                          IF(IFNULL(Libros_prestados, '') = '', '', ', '), 
                                          libro_titulo)
            WHERE Numero_documento = numero_documento;

            -- Registrar el préstamo del libro en la tabla de préstamos
            INSERT INTO prestamos (ID_libro, Documento_usuario, Fecha_prestamo) 
            VALUES (libro_id, numero_documento, fecha_prestamo);
        ELSE
            -- Manejar el caso donde el usuario no existe
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuario no encontrado.';
        END IF;
    ELSE
        -- Manejar el caso donde el libro no se encuentra
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Libro no encontrado.';
    END IF;
END//
DELIMITER ;

-- Volcando estructura para tabla biblioteca_escolar.autores
CREATE TABLE IF NOT EXISTS `autores` (
  `ID_autor` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Apellidos` varchar(255) NOT NULL,
  `Nacionalidad` varchar(50) DEFAULT NULL,
  `Fecha_nacimiento` date DEFAULT NULL,
  `Biografia` text DEFAULT NULL,
  PRIMARY KEY (`ID_autor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.autores: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
/*!40000 ALTER TABLE `autores` ENABLE KEYS */;

-- Volcando estructura para procedimiento biblioteca_escolar.BorrarUsuario
DELIMITER //
CREATE PROCEDURE `BorrarUsuario`(IN doc VARCHAR(20))
BEGIN
    -- Verifica si el usuario existe
    DECLARE usuario_existente INT;
    
    SELECT COUNT(*)
    INTO usuario_existente
    FROM usuarios
    WHERE Numero_documento = doc;
    
    IF usuario_existente > 0 THEN
        -- Elimina el usuario
        DELETE FROM usuarios
        WHERE Numero_documento = doc;
        SELECT 'Usuario eliminado correctamente' AS mensaje;
    ELSE
        -- No se encontró el usuario
        SELECT 'Usuario no encontrado' AS mensaje;
    END IF;
END//
DELIMITER ;

-- Volcando estructura para tabla biblioteca_escolar.categorias
CREATE TABLE IF NOT EXISTS `categorias` (
  `ID_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Descripcion` text DEFAULT NULL,
  PRIMARY KEY (`ID_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.categorias: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;

-- Volcando estructura para tabla biblioteca_escolar.imagenes
CREATE TABLE IF NOT EXISTS `imagenes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ID_libro` int(11) DEFAULT NULL,
  `nombre_imagen` varchar(255) DEFAULT NULL,
  `ruta_imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.imagenes: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `imagenes` DISABLE KEYS */;
REPLACE INTO `imagenes` (`id`, `ID_libro`, `nombre_imagen`, `ruta_imagen`) VALUES
	(8, NULL, '769856856772.png', 'C:/Users/311/Pictures/769856856772.png'),
	(9, NULL, '769856856772.png', 'C:/Users/311/Pictures/769856856772.png'),
	(10, 48, '2.png', 'C:/Users/311/Pictures/2.png'),
	(11, NULL, '54', '2.png');
/*!40000 ALTER TABLE `imagenes` ENABLE KEYS */;

-- Volcando estructura para procedimiento biblioteca_escolar.InsertarUsuario
DELIMITER //
CREATE PROCEDURE `InsertarUsuario`(
	IN `tipo_usuario_param` ENUM('estudiante', 'docente', 'directivo', 'publico_general'),
	IN `nombre_param` VARCHAR(100),
	IN `apellidos_param` VARCHAR(100),
	IN `tipo_documento_param` ENUM('CC', 'CE', 'PA', 'TE', 'PPT', 'PEP'),
	IN `numero_documento_param` VARCHAR(20),
	IN `fecha_nacimiento_param` DATE,
	IN `correo_electronico_param` VARCHAR(100),
	IN `contrasena_param` VARCHAR(255),
	IN `telefono_param` VARCHAR(15)
)
BEGIN
    -- Verificar si el número de documento o el correo electrónico ya existe
    DECLARE documento_existente INT;
    DECLARE correo_existente INT;

    SELECT COUNT(*)
    INTO documento_existente
    FROM usuarios
    WHERE numero_documento = numero_documento_param;

    SELECT COUNT(*)
    INTO correo_existente
    FROM usuarios
    WHERE correo_electronico = correo_electronico_param;

    IF documento_existente > 0 THEN
        -- El número de documento ya existe
        SELECT 'Número de documento ya existe' AS mensaje;
    ELSEIF correo_existente > 0 THEN
        -- El correo electrónico ya existe
        SELECT 'Correo electrónico ya existe' AS mensaje;
    ELSE
        -- Insertar nuevo usuario
        INSERT INTO usuarios (
            tipo_usuario, nombre, apellidos, fecha_nacimiento, tipo_documento, numero_documento, correo_electronico, contraseña, telefono
        ) VALUES (
            tipo_usuario_param, nombre_param, apellidos_param, fecha_nacimiento_param, tipo_documento_param, numero_documento_param, correo_electronico_param, contraseña_param, telefono_param
        );

        SELECT 'Usuario agregado correctamente' AS mensaje;
    END IF;
END//
DELIMITER ;

-- Volcando estructura para tabla biblioteca_escolar.libros
CREATE TABLE IF NOT EXISTS `libros` (
  `ID_libro` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(255) NOT NULL,
  `Autor` varchar(255) NOT NULL,
  `Año_publicacion` year(4) DEFAULT NULL,
  `Genero` varchar(50) DEFAULT NULL,
  `Resumen` text DEFAULT NULL,
  `Ejemplares_disponibles` int(11) NOT NULL DEFAULT 1,
  `Estado` enum('bueno','regular','malo') NOT NULL DEFAULT 'bueno',
  `Image_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID_libro`),
  KEY `Titulo` (`Titulo`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.libros: ~6 rows (aproximadamente)
/*!40000 ALTER TABLE `libros` DISABLE KEYS */;
REPLACE INTO `libros` (`ID_libro`, `Titulo`, `Autor`, `Año_publicacion`, `Genero`, `Resumen`, `Ejemplares_disponibles`, `Estado`, `Image_ID`) VALUES
	(1, 'Las Aventuras de María', 'Pepe', '2006', 'Terror', NULL, 1, 'bueno', NULL),
	(2, 'Pepito y sus amigos', 'Pepito2', '2032', 'Terror', '', 400, 'bueno', NULL),
	(54, '2', '2', '2002', '2', '2', 2, 'regular', NULL);
/*!40000 ALTER TABLE `libros` ENABLE KEYS */;

-- Volcando estructura para tabla biblioteca_escolar.multas
CREATE TABLE IF NOT EXISTS `multas` (
  `ID_multa` int(11) NOT NULL AUTO_INCREMENT,
  `ID_prestamo` int(11) NOT NULL,
  `Fecha_multa` date NOT NULL,
  `Valor_multa` decimal(10,2) NOT NULL,
  `Motivo` varchar(255) NOT NULL,
  `Estado` enum('pagada','pendiente') NOT NULL DEFAULT 'pendiente',
  `Fecha_pago` date DEFAULT NULL,
  PRIMARY KEY (`ID_multa`),
  KEY `ID_prestamo` (`ID_prestamo`),
  CONSTRAINT `multas_ibfk_1` FOREIGN KEY (`ID_prestamo`) REFERENCES `prestamos` (`ID_prestamo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.multas: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `multas` DISABLE KEYS */;
/*!40000 ALTER TABLE `multas` ENABLE KEYS */;

-- Volcando estructura para procedimiento biblioteca_escolar.ObtenerLibrosDisponibles
DELIMITER //
CREATE PROCEDURE `ObtenerLibrosDisponibles`()
BEGIN
    SELECT * FROM libros
    WHERE Ejemplares_disponibles > 0;
END//
DELIMITER ;

-- Volcando estructura para procedimiento biblioteca_escolar.ObtenerUbicacionImagen
DELIMITER //
CREATE PROCEDURE `ObtenerUbicacionImagen`(
    IN p_image_id INT
)
BEGIN
    SELECT ruta_imagen
    FROM imagenes
    WHERE id = p_image_id;
END//
DELIMITER ;

-- Volcando estructura para tabla biblioteca_escolar.prestamos
CREATE TABLE IF NOT EXISTS `prestamos` (
  `ID_prestamo` int(11) NOT NULL AUTO_INCREMENT,
  `ID_libro` int(11) NOT NULL,
  `Documento_usuario` varchar(20) NOT NULL DEFAULT '',
  `Fecha_prestamo` date NOT NULL,
  PRIMARY KEY (`ID_prestamo`),
  KEY `ID_libro` (`ID_libro`),
  KEY `ID_usuario` (`Documento_usuario`) USING BTREE,
  CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`ID_libro`) REFERENCES `libros` (`ID_libro`),
  CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`Documento_usuario`) REFERENCES `usuarios` (`Numero_documento`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.prestamos: ~10 rows (aproximadamente)
/*!40000 ALTER TABLE `prestamos` DISABLE KEYS */;
REPLACE INTO `prestamos` (`ID_prestamo`, `ID_libro`, `Documento_usuario`, `Fecha_prestamo`) VALUES
	(32, 1, '5962225', '2024-08-07'),
	(33, 1, '5962225', '2024-08-07'),
	(34, 1, '5962225', '2024-08-07'),
	(35, 1, '5962225', '2024-08-07'),
	(36, 1, '9876543', '2024-08-07'),
	(37, 1, '5962225', '2024-08-10'),
	(38, 1, '5962225', '2024-08-10'),
	(39, 1, '5962225', '2024-08-10'),
	(41, 1, '5962225', '2024-08-10'),
	(42, 2, '5962225', '2024-08-10');
/*!40000 ALTER TABLE `prestamos` ENABLE KEYS */;

-- Volcando estructura para tabla biblioteca_escolar.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `ID_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `Tipo_usuario` enum('estudiante','docente','directivo','publico_general') NOT NULL,
  `Nombre` varchar(255) NOT NULL,
  `Apellidos` varchar(255) NOT NULL,
  `Tipo_documento` enum('CC','CE','PA','TI','PPT','PEP') NOT NULL,
  `Numero_documento` varchar(20) NOT NULL,
  `Fecha_nacimiento` date NOT NULL,
  `Correo_electronico` varchar(255) NOT NULL,
  `Contraseña` varchar(255) NOT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `LIbros_prestados` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_usuario`),
  UNIQUE KEY `Numero_documento` (`Numero_documento`),
  UNIQUE KEY `Correo_electronico` (`Correo_electronico`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla biblioteca_escolar.usuarios: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
REPLACE INTO `usuarios` (`ID_usuario`, `Tipo_usuario`, `Nombre`, `Apellidos`, `Tipo_documento`, `Numero_documento`, `Fecha_nacimiento`, `Correo_electronico`, `Contraseña`, `Telefono`, `LIbros_prestados`) VALUES
	(1, 'estudiante', 'William Jose', 'Rivas', 'PPT', '5962225', '2007-09-26', 'williamjoserrs@gmail.com', '1234', '3195046735', ''),
	(22, 'estudiante', 'Willy', 'Rojas', 'TI', '9876543', '1600-08-07', 'willy@gmail.com', '4321', '3204264533', ''),
	(23, 'docente', 'James', 'Mosquera', 'CC', '60347266', '1982-08-24', 'james@gmail.com', '1234', '3124467324', NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

-- Volcando estructura para procedimiento biblioteca_escolar.VerificarUsuario
DELIMITER //
CREATE PROCEDURE `VerificarUsuario`(
    IN p_correo_electronico VARCHAR(255),
    IN p_contrasena VARCHAR(255),
    IN p_tipo_usuario ENUM('estudiante','docente','directivo','publico_general')
)
BEGIN
    -- Seleccionar 1 si el usuario existe, 0 si no existe
    SELECT CASE
               WHEN EXISTS (
                   SELECT 1
                   FROM usuarios
                   WHERE Correo_electronico = p_correo_electronico
                     AND Contraseña = p_contrasena
                     AND Tipo_usuario = p_tipo_usuario
               ) THEN 1
               ELSE 0
           END AS UsuarioExiste;
END//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
