from tests.functionals import AuthAsyncHTTPTestCase

class PresentationTest(AuthAsyncHTTPTestCase):

    def test_pdf(self):
        response = self.get('/labs/pdf?url=http%3A%2F%element.vagrant&setting_name=default')

        # self.assert_pdf(response)
