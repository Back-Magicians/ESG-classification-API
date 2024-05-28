# ESGify: Модель для классификации ESG-рисков

Добро пожаловать в репозиторий модели ESGify! Этот репозиторий содержит кастомную модель, построенную на основе MPNet, для классификации ESG (экологических, социальных и управленческих) рисков из текстовых данных. Модель использует среднее пуллинг и кастомную классификационную голову для получения оценок ESG-рисков.

## Обзор модели

Модель ESGify основана на архитектуре MPNet и включает кастомную классификационную голову, адаптированную для классификации ESG-рисков. Модель выдает логиты для нескольких категорий ESG-рисков, которые затем преобразуются в вероятности с помощью сигмоидной функции активации.

## Установка

### Чтобы настроить окружение для модели ESGify, выполните следующие шаги.

### Необходимые условия

- Python 3.12 или выше
- Poetry (инструмент для управления зависимостями и упаковки в Python)

### Пошаговая установка

1. Установите Poetry.

Poetry — это менеджер зависимостей для Python, который обеспечивает установку правильных зависимостей в виртуальной среде. Если у вас еще нет Poetry, вы можете установить его, выполнив:

- curl -sSL https://install.python-poetry.org | python3 -
- pip install poetry

2. Клонируйте репозиторий

- git clone https://github.com/Back-Magicians/ESG-classification-API.git
- cd esgify

3. Установите зависимости

- poetry install

4. Активируйте виртуальное окружение

- poetry shell

### Запуск через Docker

Предусмотрена возможность запуска проекта через Docker.

1. Установите Docker.
   
- Самым распространенным способом для Windows является установка через Docker Desktop, для этого перейдите на официальный сайт https://www.docker.com/products/docker-desktop.

Если у вас операционная система Linux, то выполните ряд шагов в командной строке:

- sudo apt update
- sudo apt upgrade
- sudo apt install apt-transport-https ca-certificates curl software-properties-common
- curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
- sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
- sudo apt update
- sudo apt install docker-ce
Проверьте установку.
- sudo systemctl status docker

2. Перейдите в корень проекта

3. Запустите проект

- docker-compose up -d

4. После запуска Docker контейнера проект запустится на 8000 локальном порту. 
