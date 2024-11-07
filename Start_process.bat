@echo off
echo Ejecutando comandos...

start powershell -NoExit -Command "cd Quirk_Composer\Auth0; npm start"
start powershell -NoExit -Command "cd Quirk_Composer\Quirk\out; npm run build; python3 -m http.server 4444"
start powershell -NoExit -Command "cd qweb; .\Scripts\activate; cd djangobd; python .\manage.py runserver"
start powershell -NoExit -Command "cd Quirk_Composer\Auth0\src; node .\server.js"
