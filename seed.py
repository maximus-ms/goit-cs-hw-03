from faker import Faker

from connect_pg import connect

fake = Faker('uk_UA')
USER_NUM=100
TASK_STATE_MAX=3
TASKS_PER_USER=2


def seed_db(conn):
    with conn.cursor() as cur:
        print(f"Add {USER_NUM} users ", end="", flush=True)
        for i in range(USER_NUM):
            cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fake.name(), fake.email()))
            if i % (USER_NUM//10) == 0:
                print(f".", end="", flush=True)
        print(f" done")

        print(f"Add {USER_NUM*TASKS_PER_USER} tasks ", end="", flush=True)
        for i in range(USER_NUM*TASKS_PER_USER):
            cur.execute("""INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);""",
                           (fake.sentence(nb_words=3),
                           fake.text(), fake.random.randint(1, TASK_STATE_MAX), fake.random.randint(1, USER_NUM)))
            if i % (USER_NUM*TASKS_PER_USER//10) == 0:
                print(f".", end="", flush=True)

        conn.commit()
        print(f" done")

if __name__ == '__main__':
    with connect() as conn:
        seed_db(conn)