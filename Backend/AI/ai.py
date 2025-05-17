from mistralai import Mistral
import json



def ai_parse(log):
    slice_log = log[-1000:]

    prompt = f"""
        ###### System Instructions ######
        You are a senior Linux packaging specialist with expertise in:
        - All package formats
        - Cross-distro packaging issues
        - Build systems
        - Dependency resolution across ecosystems
        
        ###### Log ######
        {slice_log}                                                                                                         

        ###### Instruction ######
        Describe the error log of the package. Write answer using this json format:
        {{
            "warnings": ["<Type of warnings that occur during assembly. It should consist of a name and a description of each warning in one single string.>],
            "errors": ["<Type of errors that occur during assembly. It should consist of a name and a description of each error  in one single string.>"],
            "mainError": "<Type of the main build error that caused the package to fail. It should consist of the name of the error and its description  in one single string.>",
            "possibleReason": "<Possible reason why that error happened.>",
            "possiblePatch": "<Possible patch that solve the problem.>"
        }}
    """


    api_key = "v0Qf8IQ33v2JFWUbsO5P8QoBzoCFk3t3"
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    s = chat_response.choices[0].message.content
    s = s.replace("```json", "").replace("```", "")
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        try:
            return json.loads(s[: e.pos])
        except Exception as e:
            raise e



def errors_description(logs):
    prompt = f"""
    ###### System Instructions ######
You are a senior Linux packaging specialist with expertise in:
- All package formats
- Cross-distro packaging issues
- Build systems
- Dependency resolution across ecosystems

###### Log ######
{logs}

###### Instruction ######
You should find meaning of clusters. So you should result in json where key is cluster id and value is string of main error reason for this cluster. Write answer using this json format:
{{
    "cluster_id": "description of the error"
}}

IMPORTANT: Make sure to use double quotes for both keys and values in the JSON.
    """

    api_key = "v0Qf8IQ33v2JFWUbsO5P8QoBzoCFk3t3"
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    
    # Получаем ответ и очищаем его от markdown разметки
    response_text = chat_response.choices[0].message.content
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    # Находим начало JSON
    start_idx = response_text.find("{")
    end_idx = response_text.rfind("}") + 1
    
    if start_idx == -1 or end_idx == 0:
        raise ValueError("No valid JSON found in the response")
    
    json_str = response_text[start_idx:end_idx]
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Если не удалось распарсить JSON, возвращаем ошибку
        raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse text: {json_str}")


