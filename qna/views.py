from rest_framework.views import APIView
from rest_framework.response import Response

from .services import answer_question


class AskQuestionView(APIView):

    def post(self, request):
        question = request.data.get("question")

        if not question:
            return Response(
                {"error": "Question is required."},
                status=400,
            )

        result = answer_question(question)

        return Response(result)