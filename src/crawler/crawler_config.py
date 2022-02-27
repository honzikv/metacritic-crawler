class CrawlerConfig:

    def __init__(self, years_crawled, max_games_per_year: int, max_critic_reviews_per_game: int,
                 max_user_reviews_per_game: int):
        self.years_crawled = years_crawled
        self.max_games_per_year = max_games_per_year
        self.max_critic_reviews_per_game = max_critic_reviews_per_game
        self.max_user_reviews_per_game = max_user_reviews_per_game
