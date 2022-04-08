from src.chat.chat import ChatDB


if __name__ == "__main__":
    result = ChatDB.find_by_message_id(1234)
    print(result)