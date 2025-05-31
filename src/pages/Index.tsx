
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Search, Users, Mail, Phone, BarChart3, Settings, Bell, Crown, Star, MapPin, Calendar, DollarSign, TrendingUp } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

// Mock data for influencers
const mockInfluencers = [
  {
    id: 1,
    name: "Sarah Johnson",
    platform: ["Instagram", "TikTok"],
    language: "English",
    followers: 125000,
    engagement_rate: 4.2,
    category: "Lifestyle & Fashion",
    location: "Los Angeles, CA",
    avg_views: 15000,
    past_collaborations: ["Nike", "Sephora", "H&M"],
    pricing: "$2,500 per post",
    preferred_contact: "Email",
    image: "/placeholder.svg"
  },
  {
    id: 2,
    name: "Alex Chen",
    platform: ["YouTube", "Instagram"],
    language: "English",
    followers: 350000,
    engagement_rate: 6.8,
    category: "Tech Reviews",
    location: "San Francisco, CA",
    avg_views: 45000,
    past_collaborations: ["Apple", "Samsung", "Tesla"],
    pricing: "$5,000 per video",
    preferred_contact: "Email",
    image: "/placeholder.svg"
  },
  {
    id: 3,
    name: "Maria Rodriguez",
    platform: ["Instagram", "YouTube"],
    language: "Spanish, English",
    followers: 89000,
    engagement_rate: 7.1,
    category: "Fitness & Wellness",
    location: "Miami, FL",
    avg_views: 12000,
    past_collaborations: ["Lululemon", "Protein World", "Nike"],
    pricing: "$1,800 per post",
    preferred_contact: "Phone",
    image: "/placeholder.svg"
  },
  {
    id: 4,
    name: "James Wilson",
    platform: ["TikTok", "Instagram"],
    language: "English",
    followers: 280000,
    engagement_rate: 8.9,
    category: "Comedy & Entertainment",
    location: "New York, NY",
    avg_views: 75000,
    past_collaborations: ["Netflix", "Spotify", "Pepsi"],
    pricing: "$4,200 per video",
    preferred_contact: "Email",
    image: "/placeholder.svg"
  }
];

const Index = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [filteredInfluencers, setFilteredInfluencers] = useState(mockInfluencers);
  const [selectedInfluencer, setSelectedInfluencer] = useState(null);
  const [emailDialogOpen, setEmailDialogOpen] = useState(false);
  const [voiceDialogOpen, setVoiceDialogOpen] = useState(false);
  const [campaignDetails, setCampaignDetails] = useState({
    brandName: '',
    campaignName: '',
    deliverables: '',
    timeline: '',
    budget: ''
  });
  const [outreachStats, setOutreachStats] = useState({
    totalOutreach: 12,
    responses: 8,
    deals: 3,
    revenue: 25000
  });

  // Authentication simulation
  const handleGoogleLogin = () => {
    setIsAuthenticated(true);
    toast({
      title: "Welcome to InfluencerFlow!",
      description: "You've successfully logged in with Google.",
    });
  };

  // Filter influencers based on search and filters
  useEffect(() => {
    let filtered = mockInfluencers;

    if (searchQuery) {
      filtered = filtered.filter(influencer =>
        influencer.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        influencer.category.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(influencer =>
        influencer.category.toLowerCase().includes(selectedCategory.toLowerCase())
      );
    }

    if (selectedPlatform !== 'all') {
      filtered = filtered.filter(influencer =>
        influencer.platform.some(p => p.toLowerCase() === selectedPlatform.toLowerCase())
      );
    }

    setFilteredInfluencers(filtered);
  }, [searchQuery, selectedCategory, selectedPlatform]);

  const handleEmailOutreach = (influencer) => {
    setSelectedInfluencer(influencer);
    setEmailDialogOpen(true);
  };

  const sendEmail = () => {
    setEmailDialogOpen(false);
    toast({
      title: "Email Sent Successfully!",
      description: `AI outreach email sent to ${selectedInfluencer?.name}. Expect a response within 24-48 hours.`,
    });
    // Simulate response after 3 seconds
    setTimeout(() => {
      toast({
        title: "Response Received!",
        description: `${selectedInfluencer?.name} replied with their phone number. Ready for voice negotiation.`,
      });
    }, 3000);
  };

  const startVoiceNegotiation = (influencer) => {
    setSelectedInfluencer(influencer);
    setVoiceDialogOpen(true);
  };

  const simulateVoiceCall = () => {
    setVoiceDialogOpen(false);
    toast({
      title: "Voice Negotiation Started!",
      description: "AI agent is now conducting the negotiation call...",
    });
    
    // Simulate call completion after 5 seconds
    setTimeout(() => {
      toast({
        title: "Negotiation Complete!",
        description: `Deal closed with ${selectedInfluencer?.name} for $3,500. Contract ready for generation.`,
      });
      // Update stats
      setOutreachStats(prev => ({
        ...prev,
        deals: prev.deals + 1,
        revenue: prev.revenue + 3500
      }));
    }, 5000);
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mb-4">
              <Crown className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-2xl font-bold">InfluencerFlow</CardTitle>
            <CardDescription>
              AI-Powered Influencer Marketing & Negotiation Platform
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={handleGoogleLogin} className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
              <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Continue with Google
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center mr-3">
                <Crown className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">InfluencerFlow</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Bell className="w-4 h-4 mr-2" />
                Notifications
              </Button>
              <Avatar>
                <AvatarFallback>BU</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs defaultValue="discovery" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-[400px]">
            <TabsTrigger value="discovery" className="flex items-center gap-2">
              <Search className="w-4 h-4" />
              Discovery
            </TabsTrigger>
            <TabsTrigger value="outreach" className="flex items-center gap-2">
              <Mail className="w-4 h-4" />
              Outreach
            </TabsTrigger>
            <TabsTrigger value="voice" className="flex items-center gap-2">
              <Phone className="w-4 h-4" />
              Voice Agent
            </TabsTrigger>
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Dashboard
            </TabsTrigger>
          </TabsList>

          {/* Discovery Tab */}
          <TabsContent value="discovery" className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Influencer Discovery</h2>
              
              {/* Search and Filters */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="md:col-span-2">
                  <Input
                    placeholder="Search influencers by name or category..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full"
                  />
                </div>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger>
                    <SelectValue placeholder="Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="lifestyle">Lifestyle & Fashion</SelectItem>
                    <SelectItem value="tech">Tech Reviews</SelectItem>
                    <SelectItem value="fitness">Fitness & Wellness</SelectItem>
                    <SelectItem value="comedy">Comedy & Entertainment</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
                  <SelectTrigger>
                    <SelectValue placeholder="Platform" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Platforms</SelectItem>
                    <SelectItem value="instagram">Instagram</SelectItem>
                    <SelectItem value="youtube">YouTube</SelectItem>
                    <SelectItem value="tiktok">TikTok</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Influencer Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredInfluencers.map((influencer) => (
                  <Card key={influencer.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader className="pb-3">
                      <div className="flex items-center space-x-3">
                        <Avatar>
                          <AvatarImage src={influencer.image} alt={influencer.name} />
                          <AvatarFallback>{influencer.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <CardTitle className="text-lg">{influencer.name}</CardTitle>
                          <div className="flex gap-1 mt-1">
                            {influencer.platform.map((platform) => (
                              <Badge key={platform} variant="secondary" className="text-xs">
                                {platform}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">Followers:</span>
                        <span className="font-medium">{influencer.followers.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">Engagement:</span>
                        <span className="font-medium text-green-600">{influencer.engagement_rate}%</span>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">Category:</span>
                        <span className="font-medium">{influencer.category}</span>
                      </div>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">Pricing:</span>
                        <span className="font-medium text-blue-600">{influencer.pricing}</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <MapPin className="w-3 h-3 mr-1" />
                        {influencer.location}
                      </div>
                      <div className="pt-3 space-y-2">
                        <Button 
                          onClick={() => handleEmailOutreach(influencer)} 
                          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                        >
                          <Mail className="w-4 h-4 mr-2" />
                          Send AI Outreach
                        </Button>
                        <Button 
                          variant="outline" 
                          onClick={() => startVoiceNegotiation(influencer)} 
                          className="w-full"
                        >
                          <Phone className="w-4 h-4 mr-2" />
                          Voice Negotiation
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Outreach</CardTitle>
                  <Mail className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{outreachStats.totalOutreach}</div>
                  <p className="text-xs text-muted-foreground">+12% from last month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Response Rate</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{Math.round((outreachStats.responses / outreachStats.totalOutreach) * 100)}%</div>
                  <p className="text-xs text-muted-foreground">+8% from last month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Deals Closed</CardTitle>
                  <Star className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{outreachStats.deals}</div>
                  <p className="text-xs text-muted-foreground">+25% from last month</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Revenue Generated</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${outreachStats.revenue.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">+30% from last month</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Negotiations</CardTitle>
                <CardDescription>Track your latest influencer outreach and negotiation results</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockInfluencers.slice(0, 3).map((influencer, index) => (
                    <div key={influencer.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Avatar>
                          <AvatarFallback>{influencer.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium">{influencer.name}</p>
                          <p className="text-sm text-gray-600">{influencer.category}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <Badge className={index === 0 ? "bg-green-100 text-green-800" : index === 1 ? "bg-yellow-100 text-yellow-800" : "bg-blue-100 text-blue-800"}>
                          {index === 0 ? "Deal Closed" : index === 1 ? "Negotiating" : "Pending Response"}
                        </Badge>
                        <p className="text-sm text-gray-600 mt-1">{influencer.pricing}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Email Outreach Dialog */}
        <Dialog open={emailDialogOpen} onOpenChange={setEmailDialogOpen}>
          <DialogContent className="sm:max-w-[525px]">
            <DialogHeader>
              <DialogTitle>AI Email Outreach</DialogTitle>
              <DialogDescription>
                Our AI agent will craft and send a personalized outreach email to {selectedInfluencer?.name}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium mb-2">Generated Email Preview:</h4>
                <p className="text-sm text-gray-700">
                  Hi {selectedInfluencer?.name},<br/><br/>
                  I hope this message finds you well! I'm reaching out from [Brand Name] because we absolutely love your content in the {selectedInfluencer?.category} space. Your engagement rates and authentic connection with your audience align perfectly with our upcoming campaign.<br/><br/>
                  We'd love to discuss a potential collaboration opportunity. Would you be available for a brief call to explore this further? Please share your preferred contact number, and we can schedule something at your convenience.<br/><br/>
                  Looking forward to potentially working together!<br/><br/>
                  Best regards,<br/>
                  AI Marketing Agent
                </p>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setEmailDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={sendEmail} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  Send Email
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* Voice Negotiation Dialog */}
        <Dialog open={voiceDialogOpen} onOpenChange={setVoiceDialogOpen}>
          <DialogContent className="sm:max-w-[525px]">
            <DialogHeader>
              <DialogTitle>AI Voice Negotiation Setup</DialogTitle>
              <DialogDescription>
                Configure your campaign details for the AI voice agent to conduct negotiations with {selectedInfluencer?.name}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="brandName">Brand Name</Label>
                  <Input
                    id="brandName"
                    placeholder="Your brand name"
                    value={campaignDetails.brandName}
                    onChange={(e) => setCampaignDetails({...campaignDetails, brandName: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="campaignName">Campaign Name</Label>
                  <Input
                    id="campaignName"
                    placeholder="Campaign title"
                    value={campaignDetails.campaignName}
                    onChange={(e) => setCampaignDetails({...campaignDetails, campaignName: e.target.value})}
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="deliverables">Deliverables</Label>
                <Textarea
                  id="deliverables"
                  placeholder="1 Instagram post, 3 stories, 1 reel..."
                  value={campaignDetails.deliverables}
                  onChange={(e) => setCampaignDetails({...campaignDetails, deliverables: e.target.value})}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="timeline">Timeline</Label>
                  <Input
                    id="timeline"
                    placeholder="2 weeks"
                    value={campaignDetails.timeline}
                    onChange={(e) => setCampaignDetails({...campaignDetails, timeline: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="budget">Budget Range</Label>
                  <Input
                    id="budget"
                    placeholder="$2,000 - $4,000"
                    value={campaignDetails.budget}
                    onChange={(e) => setCampaignDetails({...campaignDetails, budget: e.target.value})}
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setVoiceDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={simulateVoiceCall} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  <Phone className="w-4 h-4 mr-2" />
                  Start Voice Negotiation
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default Index;
