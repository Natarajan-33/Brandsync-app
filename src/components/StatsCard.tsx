
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  change: string;
  icon: LucideIcon;
  trend: 'up' | 'down' | 'neutral';
}

export function StatsCard({ title, value, change, icon: Icon, trend }: StatsCardProps) {
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600'
  };

  return (
    <Card className="border border-gray-200/60 bg-white/80 backdrop-blur-sm hover:border-purple-200 hover:shadow-lg hover:shadow-purple-100/20 transition-all duration-300 group">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center group-hover:from-purple-100 group-hover:to-blue-100 transition-colors duration-200">
          <Icon className="h-4 w-4 text-purple-600" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-gray-900">{value}</div>
        <p className={`text-xs ${trendColors[trend]} flex items-center mt-1`}>
          {change}
        </p>
      </CardContent>
    </Card>
  );
}
