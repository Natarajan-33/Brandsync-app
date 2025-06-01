
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Mail, Phone, MapPin, Users, TrendingUp, Eye, Star } from 'lucide-react';

interface InfluencerCardProps {
  influencer: {
    id: number;
    name: string;
    platform: string[];
    language: string;
    followers: number;
    engagement_rate: number;
    category: string;
    location: string;
    avg_views: number;
    past_collaborations: string[];
    pricing: string;
    preferred_contact: string;
    image: string;
  };
  onEmailOutreach: (influencer: any) => void;
  onVoiceNegotiation: (influencer: any) => void;
}

export function InfluencerCard({ influencer, onEmailOutreach, onVoiceNegotiation }: InfluencerCardProps) {
  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <Card className="group relative overflow-hidden border border-gray-200/60 bg-white/80 backdrop-blur-sm hover:border-purple-200 hover:shadow-lg hover:shadow-purple-100/20 transition-all duration-300 hover:-translate-y-1">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-50/30 to-blue-50/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <CardContent className="relative p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <Avatar className="w-12 h-12 ring-2 ring-white shadow-sm">
              <AvatarImage src={influencer.image} alt={influencer.name} />
              <AvatarFallback className="bg-gradient-to-br from-purple-500 to-blue-500 text-white font-medium">
                {influencer.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-gray-900 text-lg">{influencer.name}</h3>
              <div className="flex gap-1.5 mt-1">
                {influencer.platform.map((platform) => (
                  <Badge 
                    key={platform} 
                    variant="secondary" 
                    className="text-xs bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
                  >
                    {platform}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm font-semibold text-purple-600">{influencer.pricing}</div>
            <div className="text-xs text-gray-500">per post</div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="flex items-center gap-2 text-sm">
            <Users className="w-4 h-4 text-blue-500" />
            <div>
              <div className="font-medium text-gray-900">{formatNumber(influencer.followers)}</div>
              <div className="text-xs text-gray-500">Followers</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <TrendingUp className="w-4 h-4 text-green-500" />
            <div>
              <div className="font-medium text-green-600">{influencer.engagement_rate}%</div>
              <div className="text-xs text-gray-500">Engagement</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Eye className="w-4 h-4 text-orange-500" />
            <div>
              <div className="font-medium text-gray-900">{formatNumber(influencer.avg_views)}</div>
              <div className="text-xs text-gray-500">Avg Views</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Star className="w-4 h-4 text-yellow-500" />
            <div>
              <div className="font-medium text-gray-900">{influencer.past_collaborations.length}</div>
              <div className="text-xs text-gray-500">Collabs</div>
            </div>
          </div>
        </div>

        {/* Category & Location */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
              {influencer.category}
            </Badge>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <MapPin className="w-3 h-3" />
            {influencer.location}
          </div>
        </div>

        {/* Past Collaborations */}
        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-2">Recent collaborations:</div>
          <div className="flex flex-wrap gap-1">
            {influencer.past_collaborations.slice(0, 3).map((brand, index) => (
              <Badge key={index} variant="outline" className="text-xs bg-gray-50 text-gray-600 border-gray-200">
                {brand}
              </Badge>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button 
            onClick={() => onEmailOutreach(influencer)} 
            className="flex-1 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white border-0 shadow-sm hover:shadow-md transition-all duration-200"
            size="sm"
          >
            <Mail className="w-3.5 h-3.5 mr-2" />
            Email Outreach
          </Button>
          <Button 
            variant="outline" 
            onClick={() => onVoiceNegotiation(influencer)} 
            className="flex-1 border-gray-200 bg-white hover:bg-gray-50 transition-all duration-200"
            size="sm"
          >
            <Phone className="w-3.5 h-3.5 mr-2" />
            Voice Call
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
