# 📧 Email Setup Guide - Trading Simulator

This guide will help you set up email functionality for your Trading Simulator, including password reset and welcome emails.

## 🎯 Features Added

### ✨ New Email Features:
- **🔑 Forgot Password**: Users can reset their password via email
- **📧 Welcome Emails**: New users receive a comprehensive welcome email with usage guide
- **🔒 Secure Reset Tokens**: Time-limited, single-use password reset tokens
- **📱 Beautiful Email Templates**: Professional HTML email templates

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_email.py
```
This interactive script will guide you through the setup process.

### Option 2: Manual Setup

#### For Gmail Users:
1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to App passwords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Set Environment Variables**
   ```bash
   export EMAIL_ADDRESS="your-email@gmail.com"
   export EMAIL_PASSWORD="your-16-character-app-password"
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   ```

#### For Other Email Providers:

**Outlook/Hotmail:**
```bash
export EMAIL_ADDRESS="your-email@outlook.com"
export EMAIL_PASSWORD="your-app-password"
export SMTP_SERVER="smtp-mail.outlook.com"
export SMTP_PORT="587"
```

**Yahoo:**
```bash
export EMAIL_ADDRESS="your-email@yahoo.com"
export EMAIL_PASSWORD="your-app-password"
export SMTP_SERVER="smtp.mail.yahoo.com"
export SMTP_PORT="587"
```

## 📁 Files Added

### Core Email Files:
- `email_service.py` - Main email service with templates
- `email_config.py` - Email configuration helper
- `setup_email.py` - Interactive setup script

### Updated Files:
- `auth.py` - Added password reset and welcome email functionality
- `requirements.txt` - Added email dependencies
- `.gitignore` - Added email-related exclusions

## 🔧 Configuration

### Environment Variables:
```bash
EMAIL_ADDRESS=your-email@example.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

### Email Templates:
The system includes beautiful HTML email templates for:
- **Welcome Emails**: Comprehensive guide for new users
- **Password Reset**: Secure reset instructions with tokens

## 🧪 Testing

### Test Email Configuration:
```bash
python -c "from email_service import get_email_service; print('✅ Email configured!' if get_email_service() else '❌ Email not configured')"
```

### Test in App:
1. **Register a new user** - Check for welcome email
2. **Use "Forgot Password"** - Check for reset email
3. **Click reset link** - Test password reset flow

## 📧 Email Features

### Welcome Email Includes:
- 🎉 Welcome message and platform introduction
- 📊 Detailed guide on using stock analysis features
- 🔥 Information about popular stocks tracking
- ⭐ Favorites system explanation
- 📈 Interactive charts guide
- 💡 Pro tips for getting started
- 🔒 Security information

### Password Reset Email Includes:
- 🔒 Secure reset link with token
- ⏰ 1-hour expiration notice
- 🛡️ Security warnings and instructions
- 📱 Manual token entry option

## 🚀 Deployment

### For Streamlit Cloud:
1. **Set Environment Variables** in Streamlit Cloud dashboard:
   - Go to your app settings
   - Add the email environment variables
   - Deploy your app

2. **Update Email Links**:
   - Edit `email_service.py`
   - Replace `https://your-app-name.streamlit.app` with your actual app URL

### For Local Development:
1. Run the setup script: `python setup_email.py`
2. Start your app: `streamlit run trading_simulator.py`
3. Test the email functionality

## 🔒 Security Features

### Password Reset Security:
- **Time-limited tokens** (1 hour expiration)
- **Single-use tokens** (cannot be reused)
- **Secure token generation** using `secrets` module
- **Email verification** required for reset

### Data Protection:
- **No passwords stored in plain text**
- **Reset tokens stored separately** from user data
- **Automatic token cleanup** after use
- **Secure email transmission** via TLS

## 🐛 Troubleshooting

### Common Issues:

**"Email not configured" error:**
- Check environment variables are set
- Verify email credentials are correct
- Test with setup script

**"Failed to send email" error:**
- Check SMTP server and port settings
- Verify app password (not regular password)
- Check firewall/network restrictions

**"Invalid reset token" error:**
- Token may have expired (1 hour limit)
- Token may have been used already
- Check token format in email

### Debug Mode:
Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📱 User Experience

### For Users:
1. **Registration**: Automatic welcome email with comprehensive guide
2. **Forgot Password**: Simple email-based reset process
3. **Security**: Clear instructions and warnings
4. **Support**: Professional email templates

### For Administrators:
1. **Monitoring**: Email sending is logged
2. **Configuration**: Easy setup with interactive script
3. **Templates**: Customizable email templates
4. **Security**: Secure token management

## 🎉 Next Steps

After setup:
1. **Test the complete flow** (registration → welcome email → forgot password → reset)
2. **Customize email templates** if needed
3. **Monitor email delivery** in logs
4. **Deploy to production** with proper environment variables

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify email configuration with setup script
3. Test with a simple email first
4. Check your email provider's security settings

---

**Happy Trading! 📈**

Your users will now receive professional welcome emails and can securely reset their passwords via email!
