from dog import Dog, CONN, CURSOR

if __name__ == "__main__":
    Dog.drop_table()
    Dog.create_table()

    joey = Dog("joey", "cocker spaniel")
    joey.save()

    fanny = Dog("fanny", "cockapoo")
    fanny.save()

    import ipdb; ipdb.set_trace()