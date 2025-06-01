
import { Calendar, Users, Mail, Phone, BarChart3, Settings, Crown, Home, Search, Target, Zap } from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

const navigationItems = [
  {
    title: "Overview",
    url: "#overview",
    icon: Home,
    isActive: false,
  },
  {
    title: "Discovery",
    url: "#discovery",
    icon: Search,
    isActive: true,
  },
  {
    title: "Campaigns",
    url: "#campaigns",
    icon: Target,
    isActive: false,
  },
  {
    title: "Outreach",
    url: "#outreach",
    icon: Mail,
    isActive: false,
  },
  {
    title: "Voice Agent",
    url: "#voice",
    icon: Phone,
    isActive: false,
  },
  {
    title: "Analytics",
    url: "#analytics",
    icon: BarChart3,
    isActive: false,
  },
];

const toolsItems = [
  {
    title: "AI Assistant",
    url: "#ai",
    icon: Zap,
    isActive: false,
  },
  {
    title: "Calendar",
    url: "#calendar",
    icon: Calendar,
    isActive: false,
  },
  {
    title: "Settings",
    url: "#settings",
    icon: Settings,
    isActive: false,
  },
];

export function AppSidebar() {
  return (
    <Sidebar className="border-r border-gray-200/60 bg-white/80 backdrop-blur-xl">
      <SidebarHeader className="border-b border-gray-200/60 p-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-sm">
            <Crown className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">InfluencerFlow</h1>
            <p className="text-xs text-gray-500">AI Marketing Platform</p>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent className="px-4 py-6">
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
            Platform
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-1">
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild 
                    isActive={item.isActive}
                    className="rounded-lg font-medium transition-all duration-200 hover:bg-gray-100/80 data-[active=true]:bg-purple-50 data-[active=true]:text-purple-700 data-[active=true]:border-purple-200"
                  >
                    <a href={item.url} className="flex items-center gap-3 px-3 py-2.5">
                      <item.icon className="w-4 h-4" />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup className="mt-8">
          <SidebarGroupLabel className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
            Tools
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-1">
              {toolsItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild
                    className="rounded-lg font-medium transition-all duration-200 hover:bg-gray-100/80"
                  >
                    <a href={item.url} className="flex items-center gap-3 px-3 py-2.5">
                      <item.icon className="w-4 h-4" />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t border-gray-200/60 p-4">
        <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50/80 hover:bg-gray-100/80 transition-colors cursor-pointer">
          <Avatar className="w-8 h-8">
            <AvatarFallback className="bg-gradient-to-r from-purple-600 to-blue-600 text-white text-sm font-medium">
              BU
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">Brand User</p>
            <p className="text-xs text-gray-500 truncate">brand@company.com</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
