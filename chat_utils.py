from dataclasses import dataclass


def ask_llm(): ...


# Create dataclass thats
# question
# items yes
# item no
# Return a list of that

@dataclass
class QuestionSplit:
    question: str
    items_yes: list[str]
    items_no: list[str]

def create_questions(items: list[str], previous_questions: list[str], n: int)

def ques_and_cls_given_items(task, items: list, n, asked_ques: list = None, rest=False):
    response = get_response_method(task.guesser_model)
    if len(items) <= 1:
        return None

    asked = (
        "(The question should not be '" + "' or '".join(asked_ques) + "')"
        if asked_ques
        else ""
    )
    message = [
        {
            "role": "user",
            "content": task.prompts.generate_prompt.format(
                items_str=", ".join(items), n=n, asked=asked
            ),
        }
    ]
    print(message)
    rsp = "#" + response(message, model=task.guesser_model, max_tokens=2000)
    print([rsp])

    def process_ans(rsp):
        ans = []
        for i in range(n):
            if f"Question {i + 1}: " not in rsp:
                continue
            rsp = rsp.split(f"Question {i + 1}: ", 1)[1]
            q = rsp.split("\n", 1)[0]
            rsp = rsp.split("YES: ", 1)[1]
            if rsp[0] == "\n":
                continue
            items_y = rsp.split("\n", 1)[0].split(", ")
            items_y = list(set(items_y))
            rsp = (
                rsp.split("\nNO: ", 1)[1]
                if "\nNO: " in rsp
                else rsp.split("NO: ", 1)[1]
            )
            if rsp[0] == "\n":
                continue
            items_n = rsp.split("\n", 1)[0].split(", ")
            items_n = list(set(items_n))
            ans.append({"question": q, "items_yes": items_y, "items_no": items_n})
        return ans

    def format_rsp(rsp):
        gpt3_response = get_response_method("gpt-3.5-turbo")
        message.append({"role": "system", "content": rsp})
        message.append(
            {
                "role": "user",
                "content": task.prompts.format_generated_prompt.format(rsp=rsp),
            }
        )
        return gpt3_response(message, "gpt-3.5-turbo", max_tokens=500)

    try:
        return process_ans(rsp)
    except Exception:
        try:
            rsp = format_rsp(rsp)
            return process_ans(rsp)
        except Exception as e:
            print(e)
            return ques_and_cls_given_items(task, items, n, asked_ques, rest)
