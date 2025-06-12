Инструкция для запуска:
1. Склонируйте репозиторий
```bash
git clone <repository_url>
cd <repository_directory>
```
2. Создайте виртуальное окружение 
```bash
python -m venv venv
venv\Scripts\activate
```
3. Установите библиотеки
```bash
pip install -r requirements.txt
```
4. Запустите скрипт, указав папку с входными изображениями и опционально папку для выходных меток(по умолчанию сохранится в "./labels")
```bash
python inference.py --image_path=your_image_path --label_path=your_label_path
```
