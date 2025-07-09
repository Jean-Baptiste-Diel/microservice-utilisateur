from sqlalchemy import inspect, text
from sqlalchemy.orm.session import object_session
from app import db, app  # Assurez-vous que ces imports sont valides


def list_open_sessions():
    """Liste les sessions SQLAlchemy actives"""
    sessions = []

    # Méthode pour suivre les sessions via les objets suivis
    if hasattr(db.session, 'identity_map'):
        for obj in db.session.identity_map.values():
            session = object_session(obj)
            if session and session not in sessions:
                sessions.append({
                    "id": id(session),
                    "active": session.is_active,
                    "transaction": session.transaction and session.transaction.is_active
                })

    return sessions


def check_postgres_connections():
    """Liste les connexions PostgreSQL actives"""
    connections = []

    with app.app_context():
        try:
            result = db.session.execute(text("""
                SELECT 
                    pid, 
                    usename, 
                    application_name, 
                    state,
                    query 
                FROM pg_stat_activity 
                WHERE datname = current_database()
            """))

            # Conversion correcte des résultats en dictionnaires
            for row in result:
                connections.append({
                    'pid': row[0],
                    'user': row[1],
                    'app': row[2],
                    'state': row[3],
                    'query': row[4]
                })

        except Exception as e:
            connections.append({'error': str(e)})

    return connections


def format_output(sessions, connections):
    """Formatte les résultats pour l'affichage"""
    print("=== Sessions SQLAlchemy ===")
    if not sessions:
        print("Aucune session active détectée")
    else:
        for session in sessions:
            print(f"Session ID: {session['id']}")
            print(f"Active: {session['active']}")
            print(f"Transaction active: {session['transaction']}")
            print("-" * 40)

    print("\n=== Connexions PostgreSQL ===")
    if not connections:
        print("Aucune connexion active détectée")
    else:
        for conn in connections:
            if 'error' in conn:
                print(f"Erreur: {conn['error']}")
            else:
                print(f"PID: {conn['pid']} | User: {conn['user']}")
                print(f"App: {conn['app']} | State: {conn['state']}")
                print(f"Query: {conn['query'][:50]}...")  # Affiche les 50 premiers caractères
                print("-" * 40)


if __name__ == "__main__":
    with app.app_context():
        sessions = list_open_sessions()
        connections = check_postgres_connections()
        format_output(sessions, connections)