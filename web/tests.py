# coding: latin1
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.test import TestCase
from unittest import skip


# -------------------------------------------------------------------------------
=======
from django.contrib.auth.hashers import check_password
from django.test import TestCase, override_settings
from unittest import skip

#-------------------------------------------------------------------------------
>>>>>>> origin/djbienve

class DefaultTestCase(TestCase):
    # Inicializar la base de datos que se va a utilizar en las pruebas
    def setUp(self):
        self.username = "user1"
        self.password = "pass1"
        self.email = "false@email.com"
        User.objects.create_user(self.username, self.email, self.password)

<<<<<<< HEAD

# -------------------------------------------------------------------------------

class LoginTest(DefaultTestCase):
    def test_login_success(self):
        # Iniciar sesion con datos correctos
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la pagina principal
        self.assertRedirects(response, '/')

    def test_login_incorrect_username(self):
        # Iniciar sesion con nombre de usuario incorrecto
=======
#-------------------------------------------------------------------------------

class LoginTest(DefaultTestCase):
    def test_login_success(self):
        # Iniciar sesi�n con datos correctos
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la p�gina principal
        self.assertRedirects(response, '/')

    def test_login_incorrect_username(self):
        #Iniciar sesi�n con nombre de usuario incorrecto
>>>>>>> origin/djbienve
        response = self.client.post('/accounts/login/', {'username': 'incorrect_username', 'password': self.password})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_incorrect_password(self):
<<<<<<< HEAD
        # Iniciar sesion con password incorrecta
=======
        #Iniciar sesi�n con contrase�a incorrecta
>>>>>>> origin/djbienve
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': 'incorrect_pass'})
        self.assertNotIn('_auth_user_id', self.client.session)

    @skip("Ignorado por el momento\n")
    def test_login_logged_user(self):
<<<<<<< HEAD
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, '/')


# -------------------------------------------------------------------------------
=======
        self.client.login(username = self.username, password = self.password)
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, '/')

#-------------------------------------------------------------------------------
>>>>>>> origin/djbienve

class LogoutTest(DefaultTestCase):
    def test_logout_logged_user(self):
        # Iniciar sesion
<<<<<<< HEAD
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cerrar sesion
        response = self.client.get('/accounts/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la pagina principal
        self.assertRedirects(response, '/')

    def test_logout_not_logged_user(self):
        # Cerrar sesion sin haber iniciado sesion previamente
        response = self.client.get('/accounts/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la pagina principal
        self.assertRedirects(response, '/')


# -------------------------------------------------------------------------------

class PasswordChangeTest(DefaultTestCase):
    def test_password_change_not_logged_user(self):
        # El usuario es redigido a la pagina de login
=======
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cerrar sesi�n
        response = self.client.get('/accounts/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la p�gina principal
        self.assertRedirects(response, '/')

    def test_logout_not_logged_user(self):
        # Cerrar sesi�n sin haber iniciado sesi�n previamente
        response = self.client.get('/accounts/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)

        # El usuario es redirigido a la p�gina principal
        self.assertRedirects(response, '/')

#-------------------------------------------------------------------------------

class PasswordChangeTest(DefaultTestCase):
    def test_password_change_not_logged_user(self):
        # El usuario es redigido a la p�gina de login
>>>>>>> origin/djbienve
        response = self.client.get('/accounts/password/change/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/password/change/', target_status_code=302)

    def test_password_change_logged_user(self):
<<<<<<< HEAD
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Comprobar que se usa el template adecuado
=======
        # Iniciar sesi�n
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

>>>>>>> origin/djbienve
        response = self.client.get('/accounts/password/change/')
        self.assertTemplateUsed(response, 'web/es/password_change.html')

    def test_password_change_success(self):
        self.new_password = "new_password123"

<<<<<<< HEAD
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cambiar la password
        response = self.client.post('/accounts/password/change/',
                                    {'old_password': self.password,
                                     'new_password1': self.new_password,
                                     'new_password2': self.new_password})

        # Comprobar que el cambio se ha guardado en la base de datos
        user = User.objects.get(username=self.username)
=======
        # Iniciar sesi�n
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cambiar la contrase�a
        response = self.client.post('/accounts/password/change/',
        {'old_password' : self.password,
         'new_password1' : self.new_password,
         'new_password2' : self.new_password})

        # Comprobar que el cambio se ha guardado en la base de datos
        user = User.objects.get(username = self.username)
>>>>>>> origin/djbienve
        self.assertTrue(user.check_password(self.new_password))

        self.assertRedirects(response, '/accounts/password/change/done/')

    def test_password_change_failure(self):
<<<<<<< HEAD
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cambiar la password con datos incorrectos
        response = self.client.post('/accounts/password/change/',
                                    {'old_password': 'incorrect_old_pass',
                                     'new_password1': 'incorrect_new_pass1',
                                     'new_password2': 'incorrect_new_pass2'})

        # Comprobar que no se ha realizado ningun cambio
        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password(self.password))

        # Comprobar que se muestran los mensajes de error correspondientes
        self.assertFormError(response, 'form', 'old_password',
                             'Su contrase�a antigua es incorrecta. Por favor, vuelva a introducirla. ')
        self.assertFormError(response, 'form', 'new_password2', 'Los dos campos de contrase�a no coinciden.')


# -------------------------------------------------------------------------------

class DeleteUserTest(DefaultTestCase):
    def test_delete_user_not_logged_user(self):
        # El usuario es redigido a la pagina de login
        response = self.client.get('/accounts/user/delete/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/user/delete/', target_status_code=302)

    def test_delete_user_logged_user(self):
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Comprobar que se usa el template adecuado
        response = self.client.get('/accounts/user/delete/')
        self.assertTemplateUsed(response, 'web/es/delete_user.html')

    def test_delete_user_success(self):
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Enviar peticion de borrado con confirmacion correcta
        response = self.client.post('/accounts/user/delete/', {'username': self.username})

        # Comprobar que el usuario ha sido eliminado de la base de datos
        query = User.objects.filter(username=self.username)
        self.assertFalse(query.exists())

        # Comprobar que se ha cerrado la sesion del usuario
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_delete_user_failure(self):
        # Iniciar sesion
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Enviar peticion de borrado con confirmacion incorrecta
        response = self.client.post('/accounts/user/delete/', {'username': 'incorrect_username'})

        # Comprobar que el usuario NO ha sido eliminado de la base de datos
        query = User.objects.filter(username=self.username)
=======
        # Iniciar sesi�n
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Cambiar la contrase�a con datos incorrectos
        response = self.client.post('/accounts/password/change/',
        {'old_password' : 'incorrect_old_pass',
         'new_password1' : 'incorrect_new_pass1',
         'new_password2' : 'incorrect_new_pass2'})

        # Comprobar que no se ha realizado ning�n cambio
        user = User.objects.get(username = self.username)
        self.assertTrue(user.check_password(self.password))

        # Comprobar que se muestran los mensajes de error correspondientes
        self.assertFormError(response, 'form', 'old_password', 'Su contrase�a antigua es incorrecta. Por favor, vuelva a introducirla. ')
        self.assertFormError(response, 'form', 'new_password2', 'Los dos campos de contrase�a no coinciden.')

#-------------------------------------------------------------------------------

class DeleteUserTest(DefaultTestCase):
    def test_delete_user_not_logged_user(self):
        # El usuario es redigido a la p�gina de login
        response = self.client.get('/accounts/user/delete/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/user/delete/', target_status_code=302)

    def test_delete_user_success(self):
        # Iniciar sesi�n
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Enviar petici�n de borrado con confirmaci�n correcta
        response = self.client.post('/accounts/user/delete/', {'username' : self.username})

        # Comprobar que el usuario ha sido eliminado de la base de datos
        query = User.objects.filter(username = self.username)
        self.assertFalse(query.exists())

        # Comprobar que se ha cerrado la sesi�n del usuario
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_delete_user_failure(self):
        # Iniciar sesi�n
        self.client.login(username = self.username, password = self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Enviar petici�n de borrado con confirmaci�n incorrecta
        response = self.client.post('/accounts/user/delete/', {'username' : 'incorrect_username'})

        # Comprobar que el usuario NO ha sido eliminado de la base de datos
        query = User.objects.filter(username = self.username)
>>>>>>> origin/djbienve
        self.assertTrue(query.exists())

        # Comprobar que se muestra el mensaje de error correspondiente
        self.assertContains(response, 'El nombre de usuario introducido no coincide con tu nombre de usuario.')
