from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB URI
MONGO_URI = "mongodb://myusername:mypassword@project_mongo:27017/userdb"

# 连接到MongoDB
client = MongoClient(MONGO_URI)
db = client['userdb']

# 获取集合
users_collection = db['users']
pre_registrations_collection = db['pre_registrations']

# 查询用户信息
def get_user(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})

# 插入预挂号信息
def insert_pre_registration(user_id, existing_medical_history, department, health_analysis, main_symptoms):
    pre_registration = {
        "userId": ObjectId(user_id),
        "existingMedicalHistory": existing_medical_history,
        "department": department,
        "healthAnalysis": health_analysis,
        "mainSymptoms": main_symptoms
    }
    result = pre_registrations_collection.insert_one(pre_registration)
    return result.inserted_id

# 查询预挂号信息
def get_pre_registrations_by_user(user_id):
    return list(pre_registrations_collection.find({"userId": ObjectId(user_id)}))

# 修改预挂号信息
def update_pre_registration(pre_registration_id, existing_medical_history=None, department=None, health_analysis=None, main_symptoms=None):
    update_fields = {}
    if existing_medical_history:
        update_fields["existingMedicalHistory"] = existing_medical_history
    if department:
        update_fields["department"] = department
    if health_analysis:
        update_fields["healthAnalysis"] = health_analysis
    if main_symptoms:
        update_fields["mainSymptoms"] = main_symptoms
    
    result = pre_registrations_collection.update_one(
        {"_id": ObjectId(pre_registration_id)},
        {"$set": update_fields}
    )
    return result.modified_count

# 查询某个挂号信息中是否存在某具体元素
def get_element_in_pre_registration(pre_registration_id, element):
    pre_registration = pre_registrations_collection.find_one({"_id": ObjectId(pre_registration_id)})
    if pre_registration and element in pre_registration:
        return pre_registration[element]
    return None

# 示例用法
if __name__ == "__main__":
    # 插入数据示例
    user_id = "60c72b2f4f1a4e3d2c8b4567"  # 示例用户ID，需要替换成实际用户ID
    existing_medical_history = "每日定时服用降压药和降糖药物"
    department = "心血管内科"
    health_analysis = "血压和血糖控制相对稳定"
    main_symptoms = "最近一周出现头痛、胸闷和频繁尿频的症状"

    # 插入数据
    inserted_id = insert_pre_registration(user_id, existing_medical_history, department, health_analysis, main_symptoms)
    print(f"Inserted Pre-Registration ID: {inserted_id}")

    # 查询用户的预挂号信息
    pre_registrations = get_pre_registrations_by_user(user_id)
    for registration in pre_registrations:
        print(registration)

    # 修改预挂号信息
    modified_count = update_pre_registration(inserted_id, department="内分泌科", health_analysis="血糖略有波动")
    print(f"Number of modified documents: {modified_count}")

    # 检查某个挂号信息中是否存在某具体元素
    element_value = check_element_in_pre_registration(inserted_id, "existingMedicalHistory")
    if element_value:
        print(f"Existing Medical History: {element_value}")
    else:
        print("Element not found or not present in the pre-registration.")
