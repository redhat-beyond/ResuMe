class TestViews:
    def test_profile_view(self, client):
        response = client.get('/users/profile/')
        assert response.status_code == 302

    def test_edit_profile_view(self, client):
        response = client.get('/users/edit-profile/')
        assert response.status_code == 302
