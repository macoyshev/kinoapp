def test_admin_reachability(client_admin):
    res = client_admin.get('/admin/')

    assert res.status_code == 200
