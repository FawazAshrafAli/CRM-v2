from django.urls import path
from .views import (LoginView, LogoutView, CrmUserDetailView, 
                    Error404, Error500, MyProfileView, 
                    CrmUserFamilyUpdationView, CrmUserEducationUpdationView, 
                    CrmUserExperienceUpdationView,CrmUserUpdateView, 
                    CrmUserPersonalInfoUpdateView, CrmUserEmergencyContactUpdateView, 
                    CrmUserBankInfoUpdateView, FamilyMemberDetailView, 
                    FamilyMemberUpdateView, FamilyMemberDeleteView, 
                    EducationDetailView, EducationUpdateView, 
                    EducationDeleteView, ExperienceDetailView, 
                    ExperienceUpdateView, ExperienceDeleteView, 
                    SettingsView,LocalizationView, 
                    PaymentSettingsView, EmailSettingsView, 
                    SocialMediaLoginView, SocialLinksView, 
                    SeoSettingsView, OtherSettingsView, 
                    AddNewUserView, UpdateCustomerBasicView, 
                    RemoveCustomerLogoView, RemoveCustomerFaviconView, 
                    UpdateNumberOfUsers, DeleteUserView, 
                    UserDetailView,UpdateUsername, 
                    ChangePassword, ExpiredTemplateView, 
                    RenewAccountView, ForgotPasswordView, 
                    ResetPasswordView)

app_name = "authentication"

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # home page view    
    path('logout/', LogoutView.as_view(), name="logout"),
    # path('register/', RegisterUserView.as_view(), name="register"),
    path('detail/<pk>', CrmUserDetailView.as_view(), name="detail"),
    path('expired/', ExpiredTemplateView.as_view(), name="expired"),
    path('renew/<pk>', RenewAccountView.as_view(), name="renew"),
    path('forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('reset_password/<email>', ResetPasswordView.as_view(), name="reset_password"),

    path('update_user/', CrmUserUpdateView.as_view(), name="update_user"),
    path('update_personal_info/', CrmUserPersonalInfoUpdateView.as_view(), name="update_personal_info"),
    path('update_emergency_contacts/', CrmUserEmergencyContactUpdateView.as_view(), name="update_emergency_contacts"),
    path('update_bank_info/', CrmUserBankInfoUpdateView.as_view(), name="update_bank_info"),
    path('update_family_info/', CrmUserFamilyUpdationView.as_view(), name="update_family_info"),
    path('update_education/', CrmUserEducationUpdationView.as_view(), name="update_education"),
    path('update_experience/', CrmUserExperienceUpdationView.as_view(), name="update_experience"),

    path('family_member/<pk>', FamilyMemberDetailView.as_view(), name="family_member"),
    path('edit_family_member/<pk>', FamilyMemberUpdateView.as_view(), name="edit_family_member"),
    path('delete_family_member/<pk>', FamilyMemberDeleteView.as_view(), name="delete_family_member"),

    path('education/<pk>', EducationDetailView.as_view(), name="education"),
    path('edit_education/<pk>', EducationUpdateView.as_view(), name="edit_education"),
    path('delete_education/<pk>', EducationDeleteView.as_view(), name="delete_education"),

    path('experience/<pk>', ExperienceDetailView.as_view(), name="experience"),
    path('edit_experience/<pk>', ExperienceUpdateView.as_view(), name="edit_experience"),
    path('delete_experience/<pk>', ExperienceDeleteView.as_view(), name="delete_experience"),

    path('my_profile/', MyProfileView.as_view(), name="my_profile"),

    path('settings/', SettingsView.as_view(), name="settings"),
    path('update_customer_basic/<pk>', UpdateCustomerBasicView.as_view(), name="update_customer_basic"),
    path('update_number_of_users/<pk>', UpdateNumberOfUsers.as_view(), name="update_number_of_users"),
    path('remove_customer_logo/<pk>', RemoveCustomerLogoView.as_view(), name="remove_customer_logo"),
    path('remove_customer_favicon/<pk>', RemoveCustomerFaviconView.as_view(), name="remove_customer_favicon"),
    path('add_user/', AddNewUserView.as_view(), name="add_user"),
    path('detail_user/<pk>', UserDetailView.as_view(), name="detail_user"),
    path('delete_user/<pk>', DeleteUserView.as_view(), name="delete_user"),
    path('update_username/', UpdateUsername.as_view(), name="update_username"),
    path('change_password/', ChangePassword.as_view(), name="change_password"),

    path('localization_settings/', LocalizationView.as_view(), name="localization_settings"),
    path('payment_settings/', PaymentSettingsView.as_view(), name="payment_settings"),
    path('email_settings/', EmailSettingsView.as_view(), name="email_settings"),
    path('social_media_settings/', SocialMediaLoginView.as_view(), name="social_media_settings"),
    path('social_link_settings/', SocialLinksView.as_view(), name="social_link_settings"),
    path('seo_settings/', SeoSettingsView.as_view(), name="seo_settings"),
    path('other_settings/', OtherSettingsView.as_view(), name="other_settings"),

    path('error404', Error404.as_view(), name="error404"),
    path('error500', Error500.as_view(), name="error500"),
]
