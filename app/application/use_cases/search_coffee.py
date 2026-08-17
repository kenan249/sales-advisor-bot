class SearchCoffeeUseCase:
    def __init__(self, coffee_repository):
        self.coffee_repository = coffee_repository

    async def execute(self, parameters):
        return await self.coffee_repository.search(parameters)
