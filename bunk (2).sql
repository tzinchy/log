-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Май 07 2024 г., 21:01
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `bunk`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`%` PROCEDURE `admin_data_categor` ()   BEGIN
SELECT category.name, SUM(expense.price) FROM expense INNER JOIN category ON category.id_category = expense.category_id 
GROUP by category.name;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `create_new_expenses` (IN `p_user_id` INT, IN `p_category_id` INT, IN `p_price` DECIMAL(10,2), IN `p_date` DATE)   BEGIN 
	INSERT INTO expense (expense.user_id, expense.category_id, expense.price, expense.date_expenses)
	VALUES (p_user_id, p_category_id, p_price, p_date);
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `create_new_user` (IN `login` VARCHAR(50), IN `userPassword` VARCHAR(50))   BEGIN
    DECLARE passwordLength INT;
    SET userPassword = TRIM(userPassword);
    SET passwordLength = CHAR_LENGTH(userPassword);
	START TRANSACTION;
    IF passwordLength > 8 AND userPassword REGEXP '[0-9]' THEN
		INSERT INTO user (user.login, user.password) VALUES(login, userPassword);
        SELECT 'USER CREATED';
        COMMIT;
    ELSE 
    	SELECT 'try another password';
        ROLLBACK;
    END IF;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `data_month` ()   BEGIN 
	SELECT MONTH(expense.date_expenses), SUM(expense.price) FROM expense GROUP BY 1;
    END$$

CREATE DEFINER=`root`@`%` PROCEDURE `expenes_list` (IN `p_user_id` INT)   BEGIN 
	SELECT category.name, expense.price, expense.date_expenses FROM expense
    INNER JOIN category ON expense.category_id = category.id_category
    WHERE expense.user_id = p_user_id;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `try_to_find_user` (IN `login` VARCHAR(50), IN `user_password` VARCHAR(50))   BEGIN 
	DECLARE try_login VARCHAR(50);
    DECLARE try_password VARCHAR(50);
    SELECT user.login INTO try_login FROM user WHERE user.login = login;
    SELECT user.password INTO try_password FROM user WHERE user.login = login;
	START TRANSACTION;
    	IF (LENGTH(try_login)>0) THEN
        	IF (try_password = user_password) THEN 
        		SELECT "user exist";
                COMMIT;
            ELSE
            	SELECT 'not correct password';
                ROLLBACK;
            END IF;
        ELSE
        	SELECT "user doesnt find or doesnt exist";
            ROLLBACK;
        END IF;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `update_balance` (IN `p_id` INT, IN `price` DECIMAL(10,2))   BEGIN 
	UPDATE total_result 
    SET total_result.salary = total_result.salary + price
    WHERE total_result.user_id = p_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `admin`
--

CREATE TABLE `admin` (
  `id` int NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `admin`
--

INSERT INTO `admin` (`id`, `login`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Структура таблицы `category`
--

CREATE TABLE `category` (
  `id_category` int NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `category`
--

INSERT INTO `category` (`id_category`, `name`) VALUES
(1, 'Категория 1'),
(2, 'Категория 2'),
(3, 'Категория 3');

-- --------------------------------------------------------

--
-- Структура таблицы `expense`
--

CREATE TABLE `expense` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `category_id` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `date_expenses` date DEFAULT NULL,
  `admin_id` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `expense`
--

INSERT INTO `expense` (`id`, `user_id`, `category_id`, `price`, `date_expenses`, `admin_id`) VALUES
(1, 1, 1, '100.00', '2024-05-05', 1),
(23, 1, 2, '100.00', '2024-05-05', 1),
(24, 1, 2, '200.00', '2024-05-05', 1),
(25, 1, 2, '200.00', '2024-05-05', 1),
(26, 1, 2, '200.00', '2024-05-05', 1),
(27, 1, 2, '100.00', '2024-05-05', 1),
(28, 1, 1, '100.00', '2024-05-05', 1),
(29, 6, 2, '1000.00', '2024-05-05', 1),
(30, 1, 2, '100.00', '2024-05-05', 1),
(31, 1, 2, '1000.00', '2024-05-05', 1),
(32, 1, 1, '228.00', '2024-05-05', 1),
(33, 1, 1, '172.00', '2024-05-20', 1),
(34, 1, 1, '100.00', '2024-05-05', 1),
(35, 1, 3, '1000.00', '2024-05-06', 1),
(36, 1, 2, '1100.00', '2024-05-06', 1);

--
-- Триггеры `expense`
--
DELIMITER $$
CREATE TRIGGER `after_expense_insert` AFTER INSERT ON `expense` FOR EACH ROW BEGIN
    -- Обновляем total_expenses, добавляя значение из поля price
    UPDATE total_result
    SET total_expenses = total_expenses + NEW.price
    WHERE user_id = NEW.user_id;
    
    -- Здесь могут быть дополнительные операции по обновлению balance,
    -- если значение balance зависит от обновленного total_expenses.
    -- Предполагаем, что salary - это поле в total_result
    UPDATE total_result
    SET balance = salary - total_expenses
    WHERE user_id = NEW.user_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `total_result`
--

CREATE TABLE `total_result` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  `total_expenses` decimal(10,2) NOT NULL,
  `balance` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `total_result`
--

INSERT INTO `total_result` (`id`, `user_id`, `salary`, `total_expenses`, `balance`) VALUES
(1, 1, '5000.00', '4600.00', '400.00'),
(2, 6, '5500.00', '1000.00', '4500.00');

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`id`, `login`, `password`) VALUES
(1, 'tzinchy', 'password'),
(6, 'user', 'password8'),
(13, 'user3', 'password8');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE` (`login`);

--
-- Индексы таблицы `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id_category`);

--
-- Индексы таблицы `expense`
--
ALTER TABLE `expense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `total_result`
--
ALTER TABLE `total_result`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UNIQUE` (`login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `category`
--
ALTER TABLE `category`
  MODIFY `id_category` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `expense`
--
ALTER TABLE `expense`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `total_result`
--
ALTER TABLE `total_result`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `expense`
--
ALTER TABLE `expense`
  ADD CONSTRAINT `expense_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `expense_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id_category`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `expense_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ограничения внешнего ключа таблицы `total_result`
--
ALTER TABLE `total_result`
  ADD CONSTRAINT `total_result_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
