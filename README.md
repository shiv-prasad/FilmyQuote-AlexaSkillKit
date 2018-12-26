# FilmyQuote-AlexaSkillKit


## Setting up FilmyQuote Alexa Skill in the Developer Console

1.  **Go to the [Alexa Developer Console](http://developer.amazon.com/alexa?&sc_category=Owned&sc_channel=RD&sc_campaign=Evangelism2018&sc_publisher=github&sc_content=Survey&sc_detail=quiz-game-python-V2_GUI-1&sc_funnel=Convert&sc_country=WW&sc_medium=Owned_RD_Evangelism2018_github_Survey_quiz-game-python-V2_GUI-1_Convert_WW_beginnersdevs&sc_segment=beginnersdevs).  In the top-right corner of the screen, click the "Sign In" button.**

2.  Once you have signed in, select the **Developer Console** link and then **Alexa Skills Kit**.

3.  From the **Alexa Developer Console** select the **Create Skill** button near the top-right of the list of your Alexa Skills.

4. Give your new skill a **Name**, for example, 'Filmy Quote'. This is the name that will be shown in the Alexa Skills Store, and the name your users will refer to.

5. Select the Default Language.  This tutorial will presume you have selected 'English (US)'.

6. Select the **Custom** model under the *'Choose a model to add to your skill'* section. Click the **Create Skill** button at the top right.

7. Choose **Start from scratch** from the *Choose a template* section and click the **Choose** button on the top right.

8. **Build the Interaction Model for your skill**
	  * On the left hand navigation panel, select the **JSON Editor** tab under **Interaction Model**. In the textfield provided, replace any existing code with the code provided in the [Interaction Model](./AlexaSkill/intents.json).  Click **Save Model**.
    * If you want to change the skill invocation name, select the **Invocation** tab. Enter a **Skill Invocation Name**. This is the name that your users will need to say to start your skill.  In this case, enter 'filmy quote' as the skill invocation name.
    * Click "Build Model".

	**Note:** You should notice that **Intents** and **Slot Types** will auto populate based on the JSON Interaction Model that you have now applied to your skill. You can refer Read more about the [technical documentation](https://developer.amazon.com/docs/custom-skills/create-intents-utterances-and-slots.html?&sc_category=Owned&sc_channel=RD&sc_campaign=Evangelism2018&sc_publisher=github&sc_content=Survey&sc_detail=quiz-game-python-V2_GUI-1&sc_funnel=Convert&sc_country=WW&sc_medium=Owned_RD_Evangelism2018_github_Survey_quiz-game-python-V2_GUI-1_Convert_WW_beginnersdevs&sc_segment=beginnersdevs) to learn about **Intents**, **Slots**, and **Utterances**.

9. If your interaction model builds successfully, proceed to the next step. If not, you should see an error. Try to resolve the errors.

     If you get an error from your interaction model, check through this list:

     *  **Did you copy & paste the provided code correctly?**
     *  **Did you accidentally add any characters to the Interaction Model?**


## Setting up FilmyQuote Lambda Function in Python using Amazon Web Services

Now, we will be creating a Lambda function using [Amazon Web Services](http://aws.amazon.com). You can read more about [Lambda function](http://aws.amazon.com/lambda), but for the purposes of this guide, what you need to know is that Lambda is where our code lives.  When a user asks Alexa to use our skill, it is our Lambda function that interprets the appropriate interaction, and provides the conversation back to the user.

1.  **Go to http://aws.amazon.com and sign in to the console.** If you don't already have an account, you will need to create one.

2.  **Choose "Services" at the top of the screen, and type "Lambda" in the search box.**  You can also find it in the list of services.  It is in the "Compute" section.

    [![Lambda](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-2-services-lambda._TTH_.png)](https://console.aws.amazon.com/lambda/home)

3.  **Check your AWS region.** Lambda only works with the Alexa Skills Kit in four regions: US East (N. Virginia), EU (Ireland), US West (Oregon) and Asia Pacific (Tokyo).  Make sure you choose the region closest to your customers.

    ![Lambda Regions](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-3-check-region._TTH_.png)

4.  **Click the "Create a Lambda function" button.** It should be near the top of your screen.

    ![Create Function](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/2-4-create-a-lambda-function._TTH_.png)

5.  **Click on "Author from scratch".**  We will configure our Lambda function next.
    1. These values will only ever be visible to you, but make sure that you name your function something meaningful. "samplePythonHelloWorld" is sufficient if you don't have another idea for a name.

    2. From the "Runtime" dropdown select the python version your system supports.  This tutorial and sample code works with either Python 2.7 or 3.6. To check the python version, try the following command in a terminal
        
        ```
        $ python --version
        Python 2.7.10
        ```

    3. **Set up your Lambda function role.**  If you haven't done this before, go through the [detailed walkthrough for setting up your first role for Lambda](https://github.com/alexa/alexa-cookbook/blob/master/guides/aws-security-and-setup/lambda-role.md).  If you have done this before, you only need to select the **Existing role**.

    4. Click **Create function**.

6.  **Configure your trigger.** There are many different AWS services that can trigger a Lambda function, but for the purposes of this guide, we need to select "Alexa Skills Kit." from the left hand side.

    Once you have selected Alexa Skills Kit, scroll down and find the Skill ID verification section.  You have to paste your Alexa skill's ID in the Skill ID field.  Click the **Add** button in the lower right.  Click **Save** button in the top right corner.

7.  **Finish configuring your function**. Click on your function's name (you'll find it in the middle) and scroll to the bottom of the page, you'll see a Cloud9 code editor.

    We have provided the code for this skill on [here](./Lambda/py). To properly upload this code to Lambda, you'll need to perform the following:
    
    1. This skill uses the [ASK SDK for Python](https://github.com/alexa/alexa-skills-kit-sdk-for-python) for development. The skill code is provided in the [lambda_function.py](./Lambda/py/lambda_function.py), and the dependencies are mentioned in [requirements.txt](./Lambda/py/requirements.txt). Download the contents of the [Lambda/py](./Lambda/py) folder. 
    2. On your system, navigate to the lambda folder and install the dependencies in a new folder called “skill_env” using the following command:
    
        ```
        pip install -r py/requirements.txt -t skill_env
        ```
        
    3. Copy the contents of the `lambda/py` folder into the `skill_env` folder. 
    
        ```
        cp -r py/* skill_env/
        ```
    
    4. Zip the contents of the `skill_env` folder. Remember to zip the **contents** of the folder and **NOT** the folder itself.
    5. On the AWS Lambda console, change the **code entry type** drop-down to **Upload a .ZIP file**, upload the zip created in the previous step.
    6. Change the handler name to ``lambda_handler.handler`` and click on **Save**.

8. **As a final step, copy the ARN value from the top right corner of the screen.** You will need this value in the next step of this setup.


## Connecting Voice User Interface To FilmyQuote Lambda Function

In the first step, we created a voice user interface for the intents and utterances we expect from our users.  In the second step, we created a Lambda function that contains all of our logic for the skill.  In this step, we need to connect those two pieces together.

1.  **Go back to the [Amazon Developer Portal](https://developer.amazon.com/edw/home.html#/skills/list) and select your skill from the list.** You may still have a browser tab open if you started at the beginning of this tutorial.

2. Select the **Endpoint** tab on the left side navigation panel.

3.  **Select the "AWS Lambda ARN" option for your endpoint.**.

4.  Paste your Lambda's ARN (Amazon Resource Name) into the textbox provided for **Default Region**.

5. Click the **Save Endpoints** button at the top of the main panel.


So far, you have created a *Voice User Interface* and a *Lambda function*, and connected the two together.  Your skill is now ready to test.


## Testing Your Alexa Skill

1.  **Go back to the [Amazon Developer Portal](https://developer.amazon.com/edw/home.html#/skills/list) and select your skill from the list.**

2. Open the **Test** Pane, by selecting the **Test** link from the top navigation menu.

3. Enable Testing by activating the **Test is enabled for this skill** slider. It should be underneath the top navigation menu.

4. To validate that your skill is working as expected, invoke your skill from the **Alexa Simulator**. You can either type or click and hold the mic from the input box to use your voice.
	1. **Type** "Open" followed by the invocation name you gave your skill while setting up your skill. For example, "Open filmy quote".
	2. **Use your voice** by clicking and holding the mic on the side panel and saying "Open" followed by the invocation name you gave your skill.
	3. **If you've forgotten the invocation name** for your skill, revisit the **Build** panel on the top navigation menu and select Invocation from the sidebar to review it.

5. Ensure your skill works the way that you designed it to.
	* After you interact with the Alexa Simulator, you should see the Skill I/O **JSON Input** and **JSON Output** boxes get populated with JSON data. You can also view the **Device Log** to trace your steps.
	* If it's not working as expected, you can dig into the JSON to see exactly what Alexa is sending and receiving from the endpoint. If something is broken, AWS Lambda offers an additional testing tool to help you troubleshoot your skill.

6.  **If your sample skill is working properly, you can now customize and publish your skill.**

## Author

* **Shiv Prasad** - *Initial work* - [shiv-prasad](https://github.com/shiv-prasad/)
