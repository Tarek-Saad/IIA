# test_get_los.py

# استيراد الفئة GetLOService
from src.core.services.GetLOsService import GetLOService

# إنشاء كائن من GetLOService
lo_service = GetLOService()

# استدعاء الوظيفة مع اسم المفهوم
concept_name = "Data Structures"  # يمكنك تغيير هذا إلى أي اسم مفهوم تريد اختباره
los = lo_service.get_los_related_to_concept(concept_name)

# طباعة النتيجة للتأكد من أنها تعمل بشكل صحيح
print("Learning Objects related to the concept:", los)
