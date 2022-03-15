# import os
# from django.core.exceptions import ValidationError
# from random import choices



# def validate_file_extension(instance,value):

#     ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
#     valid_extensions = [".pdf", ".doc", ".docx", ".jpg", ".png", ".xlsx", ".xls"]
#     if instance.choices == 1:
#         if not ext.lower() == ".jpg":
#             raise ValidationError("Unsupported file extension of image!")

    # # if choices == 2:
    # #     if not ext.lower() == [".doc", ".docs"]:
    # #         raise ValidationError("Unsupported file extension of invoice!")

    # # if choices == 3:
    # #     if not ext.lower() == [".doc", ".docs"]:
    # #         raise ValidationError("Unsupported file extension of receipt!")

    # # if choices == 4:
    # #     if not ext.lower() == [".doc", ".docs"]:
    # #         raise ValidationError("Unsupported file extension of letter!") 

    # # if choices == 5:
    # #     if not ext.lower() == [".doc", ".docs"]:
    # #         raise ValidationError("Unsupported file extension of report!")                               

    # if not ext.lower() in valid_extensions:
    #     raise ValidationError("Unsupported file extension.")
