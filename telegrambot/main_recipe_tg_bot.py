from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import random
import requests
from config import tg_bot_token, open_recipe_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import BotDB
from magic_filter import F
BotDB = BotDB('error_feedback_favorites_recipe.db')
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
help_text = """
        📄 Welcome to the Bot Help Center! 📄

        🍽️ Looking for a delicious and speedy meal idea? You're in the right place! Our bot is here to provide you with a variety of quick and easy recipes for any occasion.

        🔍 How to Use:
            1. Type in your ingredient, dish name, or search by country or ethnicity.
            2. Select a recipe from the list provided.
            3. Follow the step-by-step instructions for a tasty meal in no time.

        🙋‍♂️ Need more help? Have questions about specific ingredients or cooking techniques? Feel free to ask here! Our bot is at your service to make your cooking experience enjoyable and hassle-free.

        📌 Pro Tip: Save your favorite recipes by sending them to yourself or sharing them with friends.

        Cooking made fun and simple with Quick Recipes Bot. Get ready to create culinary delights!
        """

support_text = """
        🛠 Welcome to the Bot Support Center! 🛠

        🤝 Got any questions, concerns, or need urgent assistance with the Quick Recipes Bot? We're here to lend a helping hand. Feel free to ask about scrumptious recipe recommendations, nifty troubleshooting tips, or any other inquiries related to the bot.

        ⚡ For pressing matters, don't hesitate to reach out directly to our support team at danyar.ismailov@gmail.com or in telegram @zsz_13 .

        🔧 Encountering any hiccups or noticing a little glitch while using the bot? Fret not! We've got you covered with our handy 'Mark an error' button. Your feedback plays a pivotal role in our quest for improvement!

        🚀 Our devoted support squad is all geared up to ensure a seamless and delightful experience for you. Whether it's a message ping or a phone call away, we're here!

        Bon appétit and happy cooking with Quick Recipes Bot! 🍳🥗🍔
        """


@dp.message_handler(F.text.lower() == "Mark an error")
async def inlmae(message: types.Message):
    await message.reply("/mark_an_error")


@dp.message_handler(commands=("mark_an_error", "mae", "leave_a_review", "lar", "add_to_favorites", "atf"), commands_prefix="/!")
async def record(message: types.Message):
    keyboard_answer_to_commands_mae_or_lar = types.InlineKeyboardMarkup()
    button_view_records_mae_lar = types.InlineKeyboardButton("View records", callback_data="view_records")
    button_random_recipe_mae_lar = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_answer_to_commands_mae_or_lar.add(button_view_records_mae_lar, button_random_recipe_mae_lar)
    cmd_variants = (('/mark_an_error', '/mae', '!mark_an_error', '!mae'), ('/leave_a_review', '/lar', '!leave_a_review', '!lar'), ('/add_to_favorites', '/atf', '!add_to_favorites', '!atf'))
    if message.text.startswith(cmd_variants[0]):
        operation = 'error'
    elif message.text.startswith(cmd_variants[1]):
        operation = 'review'
    elif message.text.startswith(cmd_variants[2]):
        operation = 'favorites'
    else:
        operation = 'incorrect'
    value = message.text
    print(message.from_user, ": created a record trough the command /mae or /lar with the text: ", value)
    BotDB.add_record(message.from_user.id, operation, value)
    if operation == 'error':
        await message.reply('✅ The error record has been successfully saved, thank you for your feedback! 🙏', reply_markup=keyboard_answer_to_commands_mae_or_lar)
    elif operation == 'review':
        await message.reply('✅ The review record has been successfully saved, thank you for your feedback! 🙏', reply_markup=keyboard_answer_to_commands_mae_or_lar)
    elif operation == 'favorites':
        await message.reply('✅ The record has been added to favorites! 🌟')
    else:
        await message.reply('❌ Invalid command! Please use one of the supported commands. 😢')


@dp.message_handler(commands=("delete_record", "dr"), commands_prefix="/!")
async def delete_record_by_id(message: types.Message):
    keyboard_answer_to_delete_records = types.InlineKeyboardMarkup()
    button_view_records = types.InlineKeyboardButton("View records", callback_data="view_records")
    button_random_recipe = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_answer_to_delete_records.add(button_view_records, button_random_recipe)
    args = message.get_args()
    if not args.isdigit():
        print(message.from_user, ': attempted to delete record in wrong format using the command: /dr', args)
        await message.reply("❌ Please, enter a valid numeric ID to delete a record. 🙏")
        return
    id = int(args)
    deleted = BotDB.delete_record_by_id(id)
    if deleted:
        await message.reply(f"✅ Record with ID {id} has been successfully deleted. 👍",
                            reply_markup=keyboard_answer_to_delete_records)
        print(message.from_user, ": deleted record with id", id, "through the command /delete_record")
    else:
        await message.reply(f"❌ Record with ID {id} was not found. 🤷‍♂️")
        print(message.from_user, ": attempted to delete non-existent record with id:", id)

    # await message.reply(f"✅ Record with ID {id} has been successfully deleted. 👍", reply_markup=keyboard_answer_to_delete_records)
    # print(message.from_user, ": deleted record with id " , id, "through the command /delete_record")


@dp.message_handler(commands=("records", "r"), commands_prefix="/!")
async def records(message: types.Message):
    keyboard_answer_to_view_records = types.InlineKeyboardMarkup()
    button_random_recipe_view_records = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    button_delete_all_records = types.InlineKeyboardButton("Delete all records", callback_data="delete_all_records")
    button_delete_record_by_id = types.InlineKeyboardButton("Delete one record", callback_data="delete_one_record")
    keyboard_answer_to_view_records.add(button_random_recipe_view_records, button_delete_all_records, button_delete_record_by_id)
    entries = BotDB.get_records(message.from_user.id)
    if not entries:
        await message.reply("❌ You don't have any records yet. Create some records first! 🙏")
    else:
        # formatted_records = '\n'.join(
        #     [f"Type: {record[2]}\nText: {record[3]}\nDate: {record[4]} . Record ID: {record[0]}" for record in entries])
        # await message.reply(f'✅ Please, all your records! 📋 \n{formatted_records}',
        #                           reply_markup=keyboard_answer_to_view_records)
        for record in entries:
            formatted_records = f"Type: {record[2]}\nText: {record[3]}\nDate: {record[4]} . Record ID: {record[0]}"
            await message.reply(f'✅ Please, all your records! 📋 \n{formatted_records}', reply_markup=keyboard_answer_to_view_records)
    print(message.from_user, ": watching records through the command /records")
    # entries = BotDB.get_records(message.from_user.id)
    # formatted_records = '\n'.join(
    #     [f"Type: {record[2]}\nText: {record[3]}\nDate: {record[4]} . Record ID: {record[0]}" for record in entries])
    # await message.reply(f'✅ Please, all your records! 📋 \n{formatted_records}')


@dp.message_handler(commands=("delete_all_records", "dar"), commands_prefix="/!")
async def delete_all_records(message: types.Message):
    keyboard_answer_to_delete_all_records = types.InlineKeyboardMarkup()
    button_random_recipe_delete_all_records = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_answer_to_delete_all_records.add(button_random_recipe_delete_all_records)
    # print(query.from_user)
    BotDB.delete_all_records(message.from_user.id)
    await message.reply("✅ All your records have already been deleted! 👍", reply_markup=keyboard_answer_to_delete_all_records)
    print(message.from_user, ": deleted all records through the command /delete_all_records")

random_recipe_text = ""


@dp.message_handler(commands=("random_recipe", "rr"), commands_prefix="/!")
async def get_random_recipe(message: types.Message):
    keyboard_mae_lar_atf_vr_random = types.InlineKeyboardMarkup(row_width=2)
    mark_an_error_button_random = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
    leave_a_review_button_random = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
    add_to_favorites_button_random = InlineKeyboardButton("Add to favorites from random", callback_data="add_to_favorites_from_random")
    view_records_button_random = InlineKeyboardButton("View records", callback_data="view_records")
    keyboard_mae_lar_atf_vr_random.add(mark_an_error_button_random, leave_a_review_button_random, add_to_favorites_button_random, view_records_button_random)
    dishes = ["Pizza", "Sushi", "Hamburger", "Pasta", "Chicken Rice", "Chocolate", "Ice Cream",
"Dim Sum", "Tacos", "Steak", "Fried Chicken", "Curry", "Sausages", "Ramen",
"Croissant", "Pho", "Pancakes", "Biryani", "Donuts", "Ceviche", "Tandoori Chicken",
"Shrimp Scampi", "Tofu", "Goulash", "Moussaka", "Clam Chowder", "Pad Thai", "Falafel",
"Lasagna", "Crab Cakes", "Beef Stroganoff", "Ratatouille", "Gyros", "Paella", "Hot Dog",
"Philly Cheese Steak", "Tiramisu", "Beef Wellington", "Fish and Chips", "Cordon Bleu", "Gumbo", "Peking Duck",
"Chow Mein", "Escargot", "Couscous", "Hummus", "Miso Soup", "Guacamole", "Baklava",
"Beef Bulgogi", "Kebabs", "Tom Yum Soup", "Calzone", "Lobster Bisque", "Sashimi", "Beef and Broccoli",
"Chicken Parmesan", "Cannoli", "Cobb Salad", "French Onion Soup", "Cuban Sandwich", "Red Velvet Cake", "Borscht",
"Eggs Benedict", "Corned Beef and Cabbage", "Peking Duck", "Beef Wellington", "Ravioli", "Beef Bourguignon", "Caesar Salad",
"Pierogi", "Fajitas", "Sauerbraten", "Garlic Shrimp", "Chicken Adobo", "Baba Ganoush", "Borscht",
"Gazpacho", "Crepes", "Chocolate Fondue", "Beignets", "Lentil Soup", "Butter Chicken", "Fettuccine Alfredo",
"Eggplant Parmesan", "Chicken Marsala", "Chicken Noodle Soup", "Tuna Salad", "Chicken Caesar Salad", "Garlic Bread", "Tofu Scramble",
"Lobster Roll", "Club Sandwich", "Fish Tacos", "Pumpkin Pie", "Creme Brulee", "Chicken Quesadilla", "Lamb Chops",
"Beef Tacos", "Beef Enchiladas", "Chicken Enchiladas", "Pancit", "Stuffed Bell Peppers", "Cabbage Rolls", "Egg Fried Rice",
"Shrimp Fried Rice", "Chicken Fried Rice", "Lemon Chicken", "Beef and Mushroom", "Egg Drop Soup", "Pineapple Fried Rice", "Chicken Satay",
"Stuffed Cabbage", "Chicken Teriyaki", "Baked Ziti", "Tomato Soup", "Lamb Curry", "Creamed Spinach", "Egg Salad",
"Potato Salad", "Squash Soup", "Chicken Pot Pie", "Mushroom Risotto", "Chicken Cordon Bleu", "Chicken and Rice Soup", "Lemon Meringue Pie",
"Clam Linguine", "Sausage and Peppers", "Chicken Fajitas", "Fried Rice", "Stuffed Mushrooms", "Cauliflower Soup", "Tuna Casserole",
"Chicken Kiev", "French Toast", "Beef Tacos", "Beef Stir Fry", "Chicken and Dumplings", "Chicken and Rice Casserole", "Beef and Noodles",
"Chicken Noodle Casserole", "Chicken and Sausage Gumbo", "Vegetable Stir Fry", "Creamy Tomato Soup", "Chicken and Spinach", "Chicken and Mushroom", "Chicken and Sausage Jambalaya",
"Beef and Vegetable Soup", "Chicken and Vegetable Soup", "Beef and Cabbage Soup", "Chicken and Rice Soup", "Chicken and Bacon", "Chicken and Sweet Potato"
]
    random_dish = random.choice(dishes)
    print(message.from_user, " : looks at a random recipe through the command /random_recipe  : ", random_dish)
    #write here your api_url and api_key instead of "XXX"
    api_url = 'XXXquery={}'.format(random_dish)
    api_key = 'XXX'
    r = requests.get(api_url, headers={'X-Api-Key': api_key})
    if r.status_code == requests.codes.ok:
        recipes_list = r.json()[0]
        recipe = recipes_list["title"]
        ingredients = recipes_list["ingredients"]
        instructions = recipes_list["instructions"]
        servings = recipes_list["servings"]
        global random_recipe_text
        random_recipe_text = (f"/add_to_favorites \nName of the dish: {recipe} \n\nIngredients: {ingredients}"
                            f"\n\nInstructions: {instructions} \n\nServings: {servings}")
        await message.reply(f"Please, your random recipe!\n \n🍽️ Name of the dish: {recipe} \n\n📋 Ingredients: {ingredients}"
                            f"\n\n📝 Instructions: {instructions} \n\n👥 Servings: {servings}", reply_markup=keyboard_mae_lar_atf_vr_random)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard_start = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton("Help", callback_data="help")
    button_support = types.InlineKeyboardButton("Support", callback_data="support")
    button_random_recipe_start = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_start.add(button_help, button_support, button_random_recipe_start)
    mfui = message.from_user.id
    mfuu = message.from_user.username
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    start_text = f"""
    @{mfuu}, Welcome to Recipes Bot! 🍳🌍

Type an ingredient, dish name, or even a country or ethnicity you're interested in. Our bot will fetch you some mouth watering recipes to choose from.

Happy cooking and exploring! Your ID: {mfui}
    """
    await message.reply(start_text, reply_markup=keyboard_start)
    print(message.from_user, ": pressed the command /start")


@dp.message_handler(commands=("help"), commands_prefix="/!")
async def help_command(message: types.Message):
    keyboard_start_without_help = types.InlineKeyboardMarkup()
    button_support = types.InlineKeyboardButton("Support", callback_data="support")
    button_random_recipe_start = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_start_without_help.add(button_support, button_random_recipe_start)
    await message.reply(help_text, reply_markup=keyboard_start_without_help)
    print(message.from_user, ": pressed the command /help")


@dp.message_handler(commands=("support"), commands_prefix="/!")
async def support_command(message: types.Message):
    keyboard_start_without_support = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton("Help", callback_data="help")
    button_random_recipe_start = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_start_without_support.add(button_help, button_random_recipe_start)
    await message.reply(support_text, reply_markup=keyboard_start_without_support)
    print(message.from_user, ": pressed the command /support")


@dp.callback_query_handler(text="help")
async def help_command_button(query: types.CallbackQuery):
    keyboard_start_without_help = types.InlineKeyboardMarkup()
    button_support = types.InlineKeyboardButton("Support", callback_data="support")
    button_random_recipe_start = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_start_without_help.add(button_support, button_random_recipe_start)
    await query.message.answer(help_text, reply_markup=keyboard_start_without_help)
    print(query.from_user, ': pressed the button "Help"')


@dp.callback_query_handler(text="support")
async def support_command_button(query: types.CallbackQuery):
    keyboard_start_without_support = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton("Help", callback_data="help")
    button_random_recipe_start = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    keyboard_start_without_support.add(button_help,  button_random_recipe_start)
    await query.message.answer(support_text, reply_markup=keyboard_start_without_support)
    print(query.from_user, ': pressed the button "Support"')

recipe_text = ""
recipe1_text = ""
recipe2_text = ""
recipe3_text = ""
recipe4_text = ""
recipe5_text = ""
recipe = ""
recipe1 = ""
recipe2 = ""
recipe3 = ""
recipe4 = ""
recipe5 = ""
ingredients = ""
instructions = ""
servings = ""
request_recipe = ""


@dp.message_handler()
async def get_recipe(message: types.Message):
    try:
        global recipe
        global recipe1
        global recipe2
        global request_recipe
        request_recipe = message.text
        print(message.from_user, ' : completed the request with text in the chat: ', request_recipe)
        global recipe1_text
        global recipe2_text
        # write here your api_url and api_key instead of "XXX"
        api_url = 'XXXquery={}'.format(message.text)
        api_key = 'XXX'
        r = requests.get(api_url, headers={'X-Api-Key': api_key})
        keyboard_mae_lar_atf_vr_rr_gmr = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button = InlineKeyboardButton("Add to favorites 1st recipe", callback_data="add_to_favorites_main")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        get_more_recipes_button = InlineKeyboardButton("Get more recipes of this dish", callback_data="get_more_recipes")
        keyboard_mae_lar_atf_vr_rr_gmr.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button, view_records_button, get_more_recipes_button, random_recipe_button)
        keyboard_mae_lar_atf_vr_rr_1 = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button_1 = InlineKeyboardButton("Add to favorites 2nd recipe", callback_data="add_to_favorites_main_1")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        get_more_recipes_button = InlineKeyboardButton("Get more recipes of this dish", callback_data="get_more_recipes")
        keyboard_mae_lar_atf_vr_rr_1.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button_1, view_records_button, get_more_recipes_button, random_recipe_button)
        keyboard_mae_lar_atf_vr_rr_2 = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button_2 = InlineKeyboardButton("Add to favorites 3rd recipe", callback_data="add_to_favorites_main_2")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        get_more_recipes_button = InlineKeyboardButton("Get more recipes of this dish", callback_data="get_more_recipes")
        keyboard_mae_lar_atf_vr_rr_2.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button_2, view_records_button, get_more_recipes_button,random_recipe_button)

        if r.status_code == requests.codes.ok:
            random_number0 = random.randint(1, 10)
            recipes_list = r.json()[random_number0]
            global recipe_text
            global recipe
            recipe = recipes_list["title"]
            global ingredients
            ingredients = recipes_list["ingredients"]
            global instructions
            instructions = recipes_list["instructions"]
            global servings
            servings = recipes_list["servings"]
            recipe_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe} \n\n📋 Ingredients: {ingredients}"
                                f"\n\n📝 Instructions: {instructions} \n\n👥 Servings: {servings}")

            await message.reply(f"Please, your first recipe!\n \n🍽️ Name of the dish: {recipe} \n\n📋 Ingredients: {ingredients}"
                                f"\n\n📝 Instructions: {instructions} \n\n👥 Servings: {servings}", reply_markup=keyboard_mae_lar_atf_vr_rr_gmr)

            random_number1 = random.randint(1, 10)
            recipes_list1 = r.json()[random_number1]
            recipe1 = recipes_list1["title"]
            ingredients1 = recipes_list1["ingredients"]
            instructions1 = recipes_list1["instructions"]
            servings1 = recipes_list1["servings"]
            recipe1_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe1} \n\n📋 Ingredients: {ingredients1}"
                                f"\n\n📝 Instructions: {instructions1} \n\n👥 Servings: {servings1}")

            await message.reply(
                f"Please, your second recipe!\n \n🍽️ Name of the dish: {recipe1} \n\n📋 Ingredients: {ingredients1}"
                f"\n\n📝 Instructions: {instructions1} \n\n👥 Servings: {servings1}", reply_markup=keyboard_mae_lar_atf_vr_rr_1)

            random_number2 = random.randint(1, 10)
            recipes_list2 = r.json()[random_number2]
            recipe2 = recipes_list2["title"]
            ingredients2 = recipes_list2["ingredients"]
            instructions2 = recipes_list2["instructions"]
            servings2 = recipes_list2["servings"]
            recipe2_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe2} \n\n📋 Ingredients: {ingredients2}"
                f"\n\n📝 Instructions: {instructions2} \n\n👥 Servings: {servings2}")

            await message.reply(
                f"Please, your third recipe!\n \n🍽️ Name of the dish: {recipe2} \n\n📋 Ingredients: {ingredients2}"
                f"\n\n📝 Instructions: {instructions2} \n\n👥 Servings: {servings2}", reply_markup=keyboard_mae_lar_atf_vr_rr_2)

    except:
        await message.reply("❌ Check the correctness of the name of the dish or the command, or enter the request again please 🙏 ",
                        )
    print(message.from_user, ' : got 1st recipe with the name: ', recipe)
    print(message.from_user, ' : got 2nd recipe with the name: ', recipe1)
    print(message.from_user, ' : got 3rd recipe with the name: ', recipe2)


@dp.callback_query_handler(text="mark_an_error")
async def mark_an_error_callback(query: types.CallbackQuery):
    await query.message.reply('🙏 Help us improve! Please enter /mark_an_error or /mae in the chat and describe any problems or errors you have encountered. Your feedback is invaluable in order to make our service better for everyone. Thank you for your contribution! 🚀')
    print(query.from_user, ': pressed the button "Mark an error"')


@dp.callback_query_handler(text="leave_a_review")
async def leave_a_review_callback(query: types.CallbackQuery):
    await query.message.reply('🌟 We were glad to hear from you! Please enter /leave_a_review or /lar into the chat, and then share your valuable feedback or leave a review. Your thoughts and suggestions will help us make your experience even better. Thank you for your support! 🚀')
    print(query.from_user, ': pressed the button "Leave a review"')


@dp.callback_query_handler(text="random_recipe_start")
async def random_recipe_start_callback(query: types.CallbackQuery):
    keyboard_mae_lar_atf_vr_random = types.InlineKeyboardMarkup(row_width=2)
    mark_an_error_button_random = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
    leave_a_review_button_random = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
    add_to_favorites_button_random = InlineKeyboardButton("Add to favorites from random",
                                                          callback_data="add_to_favorites_from_random")
    view_records_button_random = InlineKeyboardButton("View records", callback_data="view_records")
    keyboard_mae_lar_atf_vr_random.add(mark_an_error_button_random, leave_a_review_button_random,
                                       add_to_favorites_button_random, view_records_button_random)
    dishes = ["Pizza", "Sushi", "Hamburger", "Pasta", "Chicken Rice", "Chocolate", "Ice Cream",
              "Dim Sum", "Tacos", "Steak", "Fried Chicken", "Curry", "Sausages", "Ramen",
              "Croissant", "Pho", "Pancakes", "Biryani", "Donuts", "Ceviche", "Tandoori Chicken",
              "Shrimp Scampi", "Tofu", "Goulash", "Moussaka", "Clam Chowder", "Pad Thai", "Falafel",
              "Lasagna", "Crab Cakes", "Beef Stroganoff", "Ratatouille", "Gyros", "Paella", "Hot Dog",
              "Philly Cheese Steak", "Tiramisu", "Beef Wellington", "Fish and Chips", "Cordon Bleu", "Gumbo",
              "Peking Duck",
              "Chow Mein", "Escargot", "Couscous", "Hummus", "Miso Soup", "Guacamole", "Baklava",
              "Beef Bulgogi", "Kebabs", "Tom Yum Soup", "Calzone", "Lobster Bisque", "Sashimi", "Beef and Broccoli",
              "Chicken Parmesan", "Cannoli", "Cobb Salad", "French Onion Soup", "Cuban Sandwich", "Red Velvet Cake",
              "Borscht",
              "Eggs Benedict", "Corned Beef and Cabbage", "Peking Duck", "Beef Wellington", "Ravioli",
              "Beef Bourguignon", "Caesar Salad",
              "Pierogi", "Fajitas", "Sauerbraten", "Garlic Shrimp", "Chicken Adobo", "Baba Ganoush", "Borscht",
              "Gazpacho", "Crepes", "Chocolate Fondue", "Beignets", "Lentil Soup", "Butter Chicken",
              "Fettuccine Alfredo",
              "Eggplant Parmesan", "Chicken Marsala", "Chicken Noodle Soup", "Tuna Salad", "Chicken Caesar Salad",
              "Garlic Bread", "Tofu Scramble",
              "Lobster Roll", "Club Sandwich", "Fish Tacos", "Pumpkin Pie", "Creme Brulee", "Chicken Quesadilla",
              "Lamb Chops",
              "Beef Tacos", "Beef Enchiladas", "Chicken Enchiladas", "Pancit", "Stuffed Bell Peppers", "Cabbage Rolls",
              "Egg Fried Rice",
              "Shrimp Fried Rice", "Chicken Fried Rice", "Lemon Chicken", "Beef and Mushroom", "Egg Drop Soup",
              "Pineapple Fried Rice", "Chicken Satay",
              "Stuffed Cabbage", "Chicken Teriyaki", "Baked Ziti", "Tomato Soup", "Lamb Curry", "Creamed Spinach",
              "Egg Salad",
              "Potato Salad", "Squash Soup", "Chicken Pot Pie", "Mushroom Risotto", "Chicken Cordon Bleu",
              "Chicken and Rice Soup", "Lemon Meringue Pie",
              "Clam Linguine", "Sausage and Peppers", "Chicken Fajitas", "Fried Rice", "Stuffed Mushrooms",
              "Cauliflower Soup", "Tuna Casserole",
              "Chicken Kiev", "French Toast", "Beef Tacos", "Beef Stir Fry", "Chicken and Dumplings",
              "Chicken and Rice Casserole", "Beef and Noodles",
              "Chicken Noodle Casserole", "Chicken and Sausage Gumbo", "Vegetable Stir Fry", "Creamy Tomato Soup",
              "Chicken and Spinach", "Chicken and Mushroom", "Chicken and Sausage Jambalaya",
              "Beef and Vegetable Soup", "Chicken and Vegetable Soup", "Beef and Cabbage Soup", "Chicken and Rice Soup",
              "Chicken and Bacon", "Chicken and Sweet Potato"
              ]
    random_dish = random.choice(dishes)
    # print(random_dish)
    # write here your api_url and api_key instead of "XXX"
    api_url = 'XXXquery={}'.format(random_dish)
    api_key = 'XXX'
    r = requests.get(api_url, headers={'X-Api-Key': api_key})
    if r.status_code == requests.codes.ok:
        recipes_list = r.json()[0]
        recipe = recipes_list["title"]
        ingredients = recipes_list["ingredients"]
        instructions = recipes_list["instructions"]
        servings = recipes_list["servings"]
        global random_recipe_text
        random_recipe_text = (f"/add_to_favorites \nName of the dish: {recipe} \n\nIngredients: {ingredients}"
                              f"\n\nInstructions: {instructions} \n\nServings: {servings}")
        await query.message.reply(f"Please, your random recipe!\n \n🍽️ Name of the dish: {recipe} \n\n📋 Ingredients: {ingredients}"
                            f"\n\n📝 Instructions: {instructions} \n\n👥 Servings: {servings}", reply_markup=keyboard_mae_lar_atf_vr_random)
    print(query.from_user, ': pressed the button "Random recipe" , result: ', recipe)


@dp.callback_query_handler(text="delete_all_records")
async def delete_all_records_callback(query: types.CallbackQuery):
    keyboard_answer_to_delete_all_records = types.InlineKeyboardMarkup()
    button_random_recipe_delete_all_records = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    button_view_records_delete_all_records = types.InlineKeyboardButton("View records", callback_data="view_records")
    keyboard_answer_to_delete_all_records.add(button_random_recipe_delete_all_records, button_view_records_delete_all_records)
    # print(query.from_user)
    BotDB.delete_all_records(query.from_user.id)
    await query.message.reply("✅ All your records have already been deleted! 👍", reply_markup=keyboard_answer_to_delete_all_records)
    print(query.from_user, ': pressed the button "Delete all records"')


@dp.callback_query_handler(text="get_more_recipes")
async def get_more_recipes(query: types.CallbackQuery):
    try:
        global recipe3
        global recipe4
        global recipe5
        global request_recipe
        print(query.from_user)
        print(request_recipe)
        global recipe4_text
        global recipe5_text
        # write here your api_url and api_key instead of "XXX"
        api_url = 'XXXquery={}'.format(request_recipe)
        api_key = 'XXX'
        r = requests.get(api_url, headers={'X-Api-Key': api_key})
        keyboard_mae_lar_atf_vr_rr_3 = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button_3 = InlineKeyboardButton("Add to favorites 4th recipe", callback_data="add_to_favorites_main_3")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        # get_more_recipes_button = InlineKeyboardButton("Get more recipes", callback_data="get_more_recipes")
        keyboard_mae_lar_atf_vr_rr_3.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button_3, view_records_button, random_recipe_button)
        keyboard_mae_lar_atf_vr_rr_4 = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button_4 = InlineKeyboardButton("Add to favorites 5th recipe", callback_data="add_to_favorites_main_4")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_mae_lar_atf_vr_rr_4.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button_4, view_records_button, random_recipe_button)
        keyboard_mae_lar_atf_vr_rr_5 = types.InlineKeyboardMarkup(row_width=2)
        mark_an_error_button = InlineKeyboardButton("Mark an error", callback_data="mark_an_error")
        leave_a_review_button = InlineKeyboardButton("Leave a review", callback_data="leave_a_review")
        add_to_favorites_button_5 = InlineKeyboardButton("Add to favorites 6th recipe", callback_data="add_to_favorites_main_5")
        view_records_button = InlineKeyboardButton("View records", callback_data="view_records")
        random_recipe_button = InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_mae_lar_atf_vr_rr_5.add(mark_an_error_button, leave_a_review_button, add_to_favorites_button_5, view_records_button, random_recipe_button)

        if r.status_code == requests.codes.ok:
            random_number3 = random.randint(1, 10)
            recipes_list3 = r.json()[random_number3]
            global recipe3_text
            recipe3 = recipes_list3["title"]
            ingredients3 = recipes_list3["ingredients"]
            instructions3 = recipes_list3["instructions"]
            servings3 = recipes_list3["servings"]
            recipe3_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe3} \n\n📋 Ingredients: {ingredients3}"
                                f"\n\n📝 Instructions: {instructions3} \n\n👥 Servings: {servings3}")

            await query.message.reply(f"Please, your fourth recipe!\n \n🍽️ Name of the dish: {recipe3} \n\n📋 Ingredients: {ingredients3}"
                                f"\n\n📝 Instructions: {instructions3} \n\n👥 Servings: {servings3}", reply_markup=keyboard_mae_lar_atf_vr_rr_3)
            random_number4 = random.randint(1, 10)
            recipes_list4 = r.json()[random_number4]
            recipe4 = recipes_list4["title"]
            ingredients4 = recipes_list4["ingredients"]
            instructions4 = recipes_list4["instructions"]
            servings4 = recipes_list4["servings"]
            recipe4_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe4} \n\n📋 Ingredients: {ingredients4}"
                                f"\n\n📝 Instructions: {instructions4} \n\n👥 Servings: {servings4}")

            await query.message.reply(
                f"Please, your fifth recipe!\n \n🍽️ Name of the dish: {recipe4} \n\n📋 Ingredients: {ingredients4}"
                f"\n\n📝 Instructions: {instructions4} \n\n👥 Servings: {servings4}", reply_markup=keyboard_mae_lar_atf_vr_rr_4)

            random_number5 = random.randint(1, 10)
            recipes_list5 = r.json()[random_number5]
            recipe5 = recipes_list5["title"]
            ingredients5 = recipes_list5["ingredients"]
            instructions5 = recipes_list5["instructions"]
            servings5 = recipes_list5["servings"]
            recipe5_text = (f"/add_to_favorites \n🍽️ Name of the dish: {recipe5} \n\n📋 Ingredients: {ingredients5}"
                f"\n\n📝 Instructions: {instructions5} \n\n👥 Servings: {servings5}")

            await query.message.reply(
                f"Please, your sixth recipe!\n \n🍽️ Name of the dish: {recipe5} \n\n📋 Ingredients: {ingredients5}"
                f"\n\n📝 Instructions: {instructions5} \n\n👥 Servings: {servings5}", reply_markup=keyboard_mae_lar_atf_vr_rr_5)

    except:
        await query.message.reply("❌ Check the correctness of the name of the dish or the command, or enter the request again please 🙏 ",
                        )
    print(query.from_user, ': pressed the button "Get more recipes of this dish" , 4th recipe is: ', recipe3)
    print(query.from_user, ': pressed the button "Get more recipes of this dish" , 5th recipe is: ', recipe4)
    print(query.from_user, ': pressed the button "Get more recipes of this dish" , 6th recipe is: ', recipe5)


@dp.callback_query_handler(text="delete_one_record")
async def delete_one_record(query: types.CallbackQuery):
    await query.message.reply("🗑️ Please, enter the command /delete_record or /dr followed by a space and the ID of the record you want to delete. 🙏")
    print(query.from_user, ': pressed the button "Delete one record"')


@dp.callback_query_handler(text="view_records")
async def view_records_callback(query: types.CallbackQuery):
    keyboard_answer_to_view_records = types.InlineKeyboardMarkup()
    button_random_recipe_view_records = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
    button_delete_record_by_id = types.InlineKeyboardButton("Delete one record", callback_data="delete_one_record")
    button_delete_all_records = types.InlineKeyboardButton("Delete all records", callback_data="delete_all_records")
    keyboard_answer_to_view_records.add(button_random_recipe_view_records, button_delete_all_records, button_delete_record_by_id)
    entries = BotDB.get_records(query.from_user.id)
    if not entries:
        keyboard_answer_to_view_records_not_entries = types.InlineKeyboardMarkup()
        button_random_recipe_view_records_not_entries = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_view_records_not_entries.add(button_random_recipe_view_records_not_entries)
        await query.message.reply("❌ You don't have any records yet. Create some records first! 🙏", reply_markup=keyboard_answer_to_view_records_not_entries)
    else:
        # formatted_records = '\n'.join(
        # [f"Type: {record[2]}\nText: {record[3]}\nDate: {record[4]} . Record ID: {record[0]}" for record in entries])
        # await query.message.reply(f'✅ Please, all your records! 📋 \n{formatted_records}',reply_markup=keyboard_answer_to_view_records)
        for record in entries:
            formatted_records = f"Type: {record[2]}\nText: {record[3]}\nDate: {record[4]} . Record ID: {record[0]}"
            await query.message.reply(f'✅ Please, all your records! 📋 \n{formatted_records}', reply_markup=keyboard_answer_to_view_records)
    # await query.message.reply('📑 The "view records" command displays your favorite recipes, error reports, and feedback. Easily access these by using this command! 🧐')
    print(query.from_user, ': pressed the button "View records"')


@dp.callback_query_handler(text="add_to_favorites_from_random")
async def record_add_to_favorites_random_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_random = types.InlineKeyboardMarkup()
        button_view_records_answer = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_answer = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_random.add(button_view_records_answer, button_random_recipe_answer)
        operation = 'favorites'
        value = random_recipe_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟' , reply_markup=keyboard_answer_to_add_to_favorites_random)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
        print(query.from_user, ': pressed the button "Add to favorites from random with result: "', value)


@dp.callback_query_handler(text="add_to_favorites_main")
async def record_add_to_favorites_main_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main = types.InlineKeyboardMarkup()
        button_view_records_main = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main.add(button_view_records_main, button_random_recipe_main)
        operation = 'favorites'
        value = recipe_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟', reply_markup=keyboard_answer_to_add_to_favorites_main)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 1st recipe" with result: ', recipe)


@dp.callback_query_handler(text="add_to_favorites_main_1")
async def record_add_to_favorites_main1_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main_1 = types.InlineKeyboardMarkup()
        button_view_records_main_1 = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main_1 = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main_1.add(button_view_records_main_1, button_random_recipe_main_1)
        operation = 'favorites'
        value = recipe1_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟',reply_markup=keyboard_answer_to_add_to_favorites_main_1 )
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 2nd recipe" with result: ', recipe1)


@dp.callback_query_handler(text="add_to_favorites_main_2")
async def record_add_to_favorites_main2_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main_2 = types.InlineKeyboardMarkup()
        button_view_records_main_2 = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main_2 = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main_2.add(button_view_records_main_2, button_random_recipe_main_2)
        operation = 'favorites'
        value = recipe2_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟',reply_markup=keyboard_answer_to_add_to_favorites_main_2)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 3rd recipe" with result: ', recipe2)


@dp.callback_query_handler(text="add_to_favorites_main_3")
async def record_add_to_favorites_main3_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main_3 = types.InlineKeyboardMarkup()
        button_view_records_main_3 = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main_3 = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main_3.add(button_view_records_main_3, button_random_recipe_main_3)
        operation = 'favorites'
        value = recipe3_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟',reply_markup=keyboard_answer_to_add_to_favorites_main_3)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 4th recipe" with result: ', recipe3)


@dp.callback_query_handler(text="add_to_favorites_main_4")
async def record_add_to_favorites_main4_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main_4 = types.InlineKeyboardMarkup()
        button_view_records_main_4 = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main_4 = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main_4.add(button_view_records_main_4, button_random_recipe_main_4)
        operation = 'favorites'
        value = recipe4_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟',reply_markup=keyboard_answer_to_add_to_favorites_main_4)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 5th recipe" with result: ', recipe4)


@dp.callback_query_handler(text="add_to_favorites_main_5")
async def record_add_to_favorites_main5_callback(query: types.CallbackQuery):
    try:
        keyboard_answer_to_add_to_favorites_main_5 = types.InlineKeyboardMarkup()
        button_view_records_main_5 = types.InlineKeyboardButton("View records", callback_data="view_records")
        button_random_recipe_main_5 = types.InlineKeyboardButton("Random recipe", callback_data="random_recipe_start")
        keyboard_answer_to_add_to_favorites_main_5.add(button_view_records_main_5, button_random_recipe_main_5)
        operation = 'favorites'
        value = recipe5_text
        BotDB.add_record(query.from_user.id, operation, value)
        await query.message.reply('✅ The record already has been added to favorites! 🌟',reply_markup=keyboard_answer_to_add_to_favorites_main_5)
    except:
        await query.message.reply("❌ Check the correctness of the dish name or command. Please, try entering your request again. 🙏 ")
    print(query.from_user, ': pressed the button "Add to favorites 6th recipe" with result: ', recipe5)

if __name__ == '__main__':
    executor.start_polling(dp)


#@fastrecipe_bot username in the Telegram created by Daniyar Ismailov, danyar.ismailov@gmail.com , Telegram: @zsz_13 , github: https://github.com/zsz13
#The logo was taken from "https://www.flaticon.com/free-icons/recipe" title="recipe icons" Recipes icons created by korshun - Flaticon







