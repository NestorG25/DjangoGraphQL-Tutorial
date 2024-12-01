import graphene
from graphene_django import DjangoObjectType
from books.models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "price")
        
class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
    book = graphene.Field(BookType)
    
    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)
    
class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    message = graphene.String()
    
    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBookMutation(message="Book deleted")
        except Book.DoesNotExist:
            return DeleteBookMutation(message="Book not found")

class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)  # Book ID to update
        title = graphene.String()
        description = graphene.String()

    # The result of the mutation is the book object (return value)
    book = graphene.Field(BookType)
    message = graphene.String()

    def mutate(self, info, id, title, description):
        try:
            # Try to get the book by ID
            book = Book.objects.get(pk=id)
            if title:
                book.title = title
            if description:
                book.description = description
            book.save()
            return UpdateBookMutation(book=book, message="Book updated successfully")
        except Book.DoesNotExist:
            return UpdateBookMutation(book=None, message="Book not found")


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())
    
    def resolve_books(self, info):
        return Book.objects.all()  # Return all books
    
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)  # Return a single book by id
        
class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()
    update_book = UpdateBookMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
