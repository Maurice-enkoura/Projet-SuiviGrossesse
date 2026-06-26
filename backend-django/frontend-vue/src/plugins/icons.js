// src/plugins/icons.js
import * as LucideIcons from 'lucide-vue-next'

// Liste des icônes utilisées dans l'application
export const icons = {
  // Navigation
  Heart: LucideIcons.Heart,
  Home: LucideIcons.Home,
  Menu: LucideIcons.Menu,
  X: LucideIcons.X,
  ChevronDown: LucideIcons.ChevronDown,
  Sun: LucideIcons.Sun,
  Moon: LucideIcons.Moon,
  
  // Auth
  User: LucideIcons.User,
  Users: LucideIcons.Users,
  UserPlus: LucideIcons.UserPlus,
  UserCog: LucideIcons.UserCog,
  Lock: LucideIcons.Lock,
  Mail: LucideIcons.Mail,
  Eye: LucideIcons.Eye,
  EyeOff: LucideIcons.EyeOff,
  
  // Dashboard
  LayoutDashboard: LucideIcons.LayoutDashboard,
  Activity: LucideIcons.Activity,
  Stethoscope: LucideIcons.Stethoscope,
  Baby: LucideIcons.Baby,
  Calendar: LucideIcons.Calendar,
  CalendarPlus: LucideIcons.CalendarPlus,
  Clock: LucideIcons.Clock,
  FileText: LucideIcons.FileText,
  File: LucideIcons.File,
  FileImage: LucideIcons.FileImage,
  FilePdf: LucideIcons.FilePdf,
  MessageCircle: LucideIcons.MessageCircle,
  
  // Actions
  Plus: LucideIcons.Plus,
  Edit: LucideIcons.Edit,
  Trash2: LucideIcons.Trash2,
  Save: LucideIcons.Save,
  Download: LucideIcons.Download,
  Printer: LucideIcons.Printer,
  CheckCircle: LucideIcons.CheckCircle,
  XCircle: LucideIcons.XCircle,
  ToggleLeft: LucideIcons.ToggleLeft,
  ToggleRight: LucideIcons.ToggleRight,
  Settings: LucideIcons.Settings,
  LogOut: LucideIcons.LogOut,
  Loader2: LucideIcons.Loader2,
  ArrowLeft: LucideIcons.ArrowLeft,
  AlertCircle: LucideIcons.AlertCircle,
}

export function registerIcons(app) {
  for (const [name, component] of Object.entries(icons)) {
    app.component(name, component)
  }
}