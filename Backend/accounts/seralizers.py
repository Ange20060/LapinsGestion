from rest_framework import serializers

class loginSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=150, required=True)
  pin = serializers.CharField(min_length=6,max_length=6,write_only=True,trim_whitespace=False,required=True)

  def validate_pin(self, value):
    if not value.isdigit():
      raise serializers.ValidationError("Le PIN doit être composé uniquement de 6 chiffres.")
    return value

class SetPinSerializer(serializers.Serializer):
  pin = serializers.CharField(min_length=6,max_length=6,write_only=True,trim_whitespace=False,required=True)
  confirmation = serializers.CharField(min_length=6,max_length=6,write_only=True,trim_whitespace=False,required=True)

  def validate_pin(self, value):
    if not value.isdigit():
      raise serializers.ValidationError("Le PIN doit être composé uniquement de 6 chiffres.")
    return value

  def validate_confirmation(self, value):
    if not value.isdigit():
      raise serializers.ValidationError("La confirmation du PIN doit être composée uniquement de 6 chiffres.")
    return value

  def validate(self, data):
    if data['pin'] != data['confirmation']:
      raise serializers.ValidationError("Les PIN et confirmation ne correspondent pas.")
    return data
