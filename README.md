# 💰 Telegram Expense Tracker

A modern, minimalist expense tracking application built for Telegram Mini Apps with a clean black and white design and rounded corners.

## ✨ Features

- 📱 **Mobile-First Design** - Optimized for Telegram Mini Apps
- 🎨 **Minimalist UI** - Pure black and white with rounded corners
- 📊 **Expense Tracking** - Add, view, and manage expenses
- 📈 **Statistics** - View spending analytics and category breakdowns
- 🏷️ **Categories** - Organize expenses with predefined categories
- 💳 **Bank Balance** - Track your bank balance alongside expenses
- 🔄 **Real-time Updates** - Instant updates with observer pattern

## 🏗️ Architecture

Built with clean architecture principles:

- **MVC Pattern** - Model-View-Controller separation
- **Repository Pattern** - Data access abstraction
- **Service Layer** - Business logic separation
- **Factory Pattern** - Object creation management
- **Observer Pattern** - Event-driven updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Flask
- Telegram Bot Token

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/telegram-expense-tracker.git
cd telegram-expense-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export BOT_TOKEN="your_telegram_bot_token"
```

4. Run the application:
```bash
python app.py
```

## 🌐 Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `BOT_TOKEN`: Your Telegram bot token
   - `FLASK_ENV`: production
   - `FLASK_DEBUG`: False

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📱 Usage

1. **Add Expenses**: Enter amount, select category, add description
2. **View Expenses**: See recent expenses with category icons
3. **Statistics**: Track spending patterns and category breakdowns
4. **Settings**: Manage app preferences and view information

## 🎨 Design

- **Color Scheme**: Pure black (#000000) and white (#ffffff)
- **Typography**: System fonts for optimal readability
- **Layout**: Single-page design with centered text
- **Components**: Rounded corners (10px-20px) for modern look
- **Responsive**: Mobile-first design approach

## 📁 Project Structure

```
snake/
├── api/
│   └── index.py          # Vercel entry point
├── templates/
│   └── index.html        # Frontend template
├── models.py             # Data models
├── repository.py         # Data access layer
├── services.py           # Business logic
├── controllers.py        # Request handlers
├── observers.py          # Event system
├── app.py               # Flask application
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 API Endpoints

- `GET /` - Main application interface
- `POST /api/init` - Initialize user session
- `GET /api/expenses` - Get user expenses
- `POST /api/expenses` - Add new expense
- `DELETE /api/expenses/<id>` - Delete expense
- `GET /api/categories` - Get expense categories
- `GET /api/stats` - Get user statistics
- `GET /api/balance` - Get bank balance
- `POST /api/balance` - Update bank balance
- `GET /health` - Health check

## 🛠️ Development

### Adding New Features

1. Create model in `models.py`
2. Add repository methods in `repository.py`
3. Implement business logic in `services.py`
4. Add controller endpoints in `controllers.py`
5. Update frontend in `templates/index.html`

### Testing

```bash
python -c "import models, repository, services, controllers, observers; print('✅ All modules imported successfully')"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support, please open an issue on GitHub or contact the maintainer.

## 🎯 Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Data export (CSV, PDF)
- [ ] Budget tracking
- [ ] Recurring expenses
- [ ] Multi-currency support
- [ ] Dark mode toggle

---

**Version**: 1.0.0  
**Last Updated**: October 2024  
**Maintainer**: Your Name
