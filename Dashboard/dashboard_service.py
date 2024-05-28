from utils.loggings import log_creator

def fetch_data(db, query, params):
    try:
        result = db.fetch(query, params)
        return result
    except Exception as e:
        log_creator(api_key=params[0], name='Unknown', log=str(e), error=True)
        return None

def portfolio(db, api_key, stock=None):
    query = 'SELECT * FROM stocks WHERE api_key = %s'
    params = (api_key,)
    if stock is not None:
        query += ' AND stock = %s'
        params += (stock,)
    
    result = fetch_data(db, query, params)
    if result and result not in [[]]:
        log_creator(api_key=api_key, name=result[0][2], log='Portfolio fetched', error=False)
        portfolio = []
        for row in result:
            portfolio.append({
                "Stock": row[3],
                "Quantity": row[4]
            })
        return portfolio
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to fetch portfolio', error=True)
        return None

def transaction(db, api_key, stock=None, transaction_type=None, start_date=None, end_date=None):
    query = 'SELECT * FROM trades WHERE api_key = %s'

    params = (api_key,)
    if stock is not None:
        query += ' AND stock = %s'
        params += (stock,)
    if transaction_type is not None:
        query += ' AND type = %s'
        params += (transaction_type,)
    if start_date is not None:
        query += ' AND time >= %s'
        params += (start_date,)
    if end_date is not None:
        query += ' AND time <= %s'
        params += (end_date,)
    query += ' ORDER BY time DESC'
    
    result = fetch_data(db, query, params)
    if result and result not in [[]]:
        log_creator(api_key=api_key, name='Unknown', log='Transaction fetched', error=False)
        transactions = []
        for row in result:
            transactions.append({
                "Stock": row[3],
                "Stock_price": row[4],
                "Quantity": row[5],
                "Type": row[6],
                "before_balance": row[7],
                "After_balance": row[8],
                "Time": row[9]
            })
        return transactions
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to fetch transactions', error=True)
        return None

def get_user(db, api_key):
    query = 'SELECT * FROM users WHERE api_key = %s'
    result = fetch_data(db, query, (api_key,))
    if result and result not in [[]]:
        log_creator(api_key=api_key, name=result[0][1], log='User data fetched', error=False)
        return {
            "api_key": result[0][0],
            "name": result[0][1],
            "team": result[0][2],
            "balance": result[0][3],
            "token": result[0][4],
            "token_expiry": result[0][5]
        }
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to fetch user data', error=True)
        return None

def get_user_data(db, team):
    query = 'SELECT * FROM users WHERE team = %s'
    result = fetch_data(db, query, (team,))
    if result and result not in [[]]:
        log_creator(api_key="unknown", name='Unknown', log='User data fetched', error=False)
        users = []
        for row in result:
            users.append({
                "api_key": row[0],
                "name": row[1],
                "team": row[2],
                "balance": row[3],
                "token": row[4],
                "token_expiry": row[5]
            })
        return users
    else:
        log_creator(api_key="unknown", name='Unknown', log='Failed to fetch user data', error=True)
        return None

def dashboard_result(db, team):
    user_data = get_user_data(db, team)
    if user_data and user_data not in [[]]:
        log_creator(api_key="unknown", name=team, log='Dashboard data fetched', error=False)
        dashboard = []
        for user in user_data:
            dashboard.append({
                "Name": user["name"],
                "Team": user["team"],
                "Balance": user["balance"],
            })
        return dashboard
    else:
        log_creator(api_key="unknown", name=team, log='Failed to fetch dashboard data', error=True)
        return None


    