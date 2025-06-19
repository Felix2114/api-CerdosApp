import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from cerdos.models import Cerdos, Vote, Comment
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

class CerdosType(DjangoObjectType):
    class Meta:
        model = Cerdos

class CountableConnectionBase(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ('user', 'cerdos')
        filter_fields = ('user', 'cerdos')
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnectionBase

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    cerdos = graphene.List(
        CerdosType,
        search=graphene.String(),
       first=graphene.Int(),
       skip=graphene.Int(),
       )
    
    #votes = graphene.List(VoteType)
    votes = DjangoFilterConnectionField(VoteType)
    comments = graphene.List(CommentType)

    def resolve_cerdos(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Cerdos.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]
    
        return qs

    
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()
    
    def resolve_comments(self, info, cerdos_id=None, **kwargs):
         if cerdos_id:
              return Comment.objects.filter(cerdos__id=cerdos_id)
         return Comment.objects.all()
    

class CreateCerdo(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    nombre = graphene.String()
    raza = graphene.String()
    peso = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()
        nombre = graphene.String()
        raza = graphene.String()
        peso = graphene.String()

    def mutate(self, info, url, description, nombre, raza, peso):
        user = info.context.user or None
        if user.is_anonymous:
           raise GraphQLError("You must be logged in to create a cerdo.")

        cerdos = Cerdos(
              url=url,
              description=description,
              nombre=nombre, 
              raza=raza, 
              peso=peso,
              posted_by=user,
              )
        cerdos.save()

        return CreateCerdo(
            id=cerdos.id,
            url=cerdos.url,
            description=cerdos.description,
            nombre=cerdos.nombre,
            raza=cerdos.raza,
            peso=cerdos.peso,
            posted_by=cerdos.posted_by,
        )
    

# Add the CreateVote mutation
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    cerdos = graphene.Field(CerdosType)

    class Arguments:
        cerdos_id = graphene.Int()

    def mutate(self, info, cerdos_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        cerdos = Cerdos.objects.filter(id=cerdos_id).first()
        if not cerdos:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            cerdos=cerdos,
        )

        return CreateVote(user=user, cerdos=cerdos)
    

class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        cerdos_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    
    def mutate(self, info, cerdos_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        cerdos = Cerdos.objects.get(id=cerdos_id)
        if not cerdos:
            raise Exception('Invalid Link!')
        
        comment = Comment.objects.create(
               user=user,
               cerdos=cerdos, 
               content=content,
        )

        return CreateComment(comment=comment)



class Mutation(graphene.ObjectType):
    create_cerdo = CreateCerdo.Field()
    create_vote = CreateVote.Field()
    create_comment = CreateComment.Field()