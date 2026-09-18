from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AssistantFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='StrongPass123!',
            is_staff=True,
        )
        self.client.login(username='adminuser', password='StrongPass123!')

    def test_assistant_answers_common_garden_questions(self):
        response = self.client.post(reverse('assistant'), {'question': 'Why are my leaves yellow?'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yellow leaves')
        self.assertContains(response, 'Check soil moisture')

    def test_garden_manager_page_includes_assistant_panel(self):
        response = self.client.get(reverse('garden_manager'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Garden assistant')

    def test_staff_manager_redirects_to_project_login_page(self):
        self.client.logout()
        response = self.client.get(reverse('garden_manager'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/garden-manager/', fetch_redirect_response=False)
