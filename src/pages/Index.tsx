
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Search, Crown, Mail, Phone, DollarSign, TrendingUp, Users, Star } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/AppSidebar';
import { InfluencerCard } from '@/components/InfluencerCard';
import { StatsCard } from '@/components/StatsCard';

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
    pricing: "$2,500",
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
    pricing: "$5,000",
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
    pricing: "$1,800",
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
    pricing: "$4,200",
    preferred_contact: "Email",
    image: "/placeholder.svg"
  }
];

const Index = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInputValue, setSearchInputValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [filteredInfluencers, setFilteredInfluencers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
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

  // Function to fetch influencers from the backend API
  const fetchInfluencers = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      let url = 'http://localhost:8000/influencers';
      
      // If there's a search query, use the semantic search endpoint
      if (searchInputValue.trim()) {
        // Build a natural language query that includes all filters
        let fullQuery = searchInputValue;
        
        // Add category and platform to the search query if selected
        if (selectedCategory !== 'all') {
          fullQuery += ` in category ${selectedCategory}`;
        }
        
        if (selectedPlatform !== 'all') {
          fullQuery += ` on ${selectedPlatform}`;
        }
        
        url = `http://localhost:8000/influencers/search?q=${encodeURIComponent(fullQuery)}`;
      }
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error('Failed to fetch influencers');
      }
      
      let data = await response.json();
      
      // If we're not using semantic search, apply client-side filtering
      if (!searchInputValue.trim()) {
        // Apply category filter
        if (selectedCategory !== 'all') {
          data = data.filter(influencer => 
            influencer.category.toLowerCase().includes(selectedCategory.toLowerCase())
          );
        }
        
        // Apply platform filter
        if (selectedPlatform !== 'all') {
          data = data.filter(influencer => {
            // Handle both array and string formats for platforms
            if (Array.isArray(influencer.platforms)) {
              return influencer.platforms.some(p => 
                p.toLowerCase().includes(selectedPlatform.toLowerCase())
              );
            } else if (typeof influencer.platforms === 'string') {
              return influencer.platforms.toLowerCase().includes(selectedPlatform.toLowerCase());
            }
            return false;
          });
        }
      }
      
      // Map backend data to frontend format if needed
      const mappedData = data.map(influencer => ({
        id: influencer.id,
        name: influencer.name,
        platform: Array.isArray(influencer.platforms) ? influencer.platforms : influencer.platforms.split(', '),
        language: 'English', // Default value as this might not be in the backend
        followers: influencer.followers,
        engagement_rate: influencer.engagement_rate,
        category: influencer.category,
        location: influencer.region,
        avg_views: Math.round(influencer.followers * (influencer.engagement_rate / 100)), // Estimate
        past_collaborations: [], // Not available in backend data
        pricing: influencer.rate_card,
        preferred_contact: 'Email',
        image: '/placeholder.svg'
      }));
      
      setFilteredInfluencers(mappedData);
    } catch (err) {
      console.error('Error fetching influencers:', err);
      setError(err.message);
      // Fall back to mock data if API fails
      setFilteredInfluencers(mockInfluencers);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Fetch initial data when component mounts
  useEffect(() => {
    fetchInfluencers();
  }, []);
  
  // We don't need this useEffect since we'll call fetchInfluencers directly from the button

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
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center p-4">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(147,51,234,0.1),transparent_70%)]" />
        <Card className="w-full max-w-md relative border-0 shadow-2xl shadow-purple-500/10 bg-white/80 backdrop-blur-xl">
          <CardHeader className="text-center pb-8 pt-8">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-purple-500/25">
              <Crown className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              InfluencerFlow
            </CardTitle>
            <CardDescription className="text-gray-600 mt-2 text-lg">
              AI-Powered Influencer Marketing & Negotiation Platform
            </CardDescription>
          </CardHeader>
          <CardContent className="pb-8">
            <Button 
              onClick={handleGoogleLogin} 
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 h-12 text-base font-medium"
            >
              <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
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
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gradient-to-br from-gray-50 via-white to-purple-50">
        <AppSidebar />
        <SidebarInset className="flex-1">
          {/* Header */}
          <header className="border-b border-gray-200/60 bg-white/80 backdrop-blur-xl sticky top-0 z-10">
            <div className="flex h-16 items-center gap-4 px-6">
              <SidebarTrigger className="w-8 h-8" />
              <div className="flex-1">
                <h2 className="text-xl font-semibold text-gray-900">Influencer Discovery</h2>
                <p className="text-sm text-gray-500">Find and connect with creators for your campaigns</p>
              </div>
            </div>
          </header>

          <main className="flex-1 p-6">
            <Tabs defaultValue="discovery" className="space-y-6">
              <TabsList className="bg-white/80 backdrop-blur-sm border border-gray-200/60 p-1 rounded-xl shadow-sm">
                <TabsTrigger value="discovery" className="rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-blue-600 data-[state=active]:text-white transition-all duration-200">
                  <Search className="w-4 h-4 mr-2" />
                  Discovery
                </TabsTrigger>
                <TabsTrigger value="dashboard" className="rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-blue-600 data-[state=active]:text-white transition-all duration-200">
                  <TrendingUp className="w-4 h-4 mr-2" />
                  Analytics
                </TabsTrigger>
              </TabsList>

              {/* Discovery Tab */}
              <TabsContent value="discovery" className="space-y-6">
                <Card className="border border-gray-200/60 bg-white/80 backdrop-blur-sm shadow-sm">
                  <CardContent className="p-6">
                    {/* Search and Filters */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                      <div className="md:col-span-2 flex gap-2">
                        <div className="relative flex-1">
                          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                          <Input
                            placeholder="Search influencers by name or category..."
                            value={searchInputValue}
                            onChange={(e) => setSearchInputValue(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                setSearchQuery(searchInputValue);
                                fetchInfluencers();
                              }
                            }}
                            className="pl-10 border-gray-200 bg-white/80 backdrop-blur-sm focus:border-purple-300 focus:ring-purple-200 transition-all duration-200"
                          />
                        </div>
                        <Button 
                          onClick={() => {
                            setSearchQuery(searchInputValue);
                            fetchInfluencers();
                          }}
                          className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white"
                          disabled={isLoading}
                        >
                          {isLoading ? 'Searching...' : 'Search'}
                        </Button>
                      </div>
                      <div className="md:col-span-2 grid grid-cols-2 gap-4">
                        <Select value={selectedCategory} onValueChange={(value) => setSelectedCategory(value)}>
                          <SelectTrigger className="border-gray-200 bg-white/80 backdrop-blur-sm focus:border-purple-300 focus:ring-purple-200">
                            <SelectValue placeholder="Category" />
                          </SelectTrigger>
                          <SelectContent className="bg-white/95 backdrop-blur-sm border-gray-200">
                            <SelectItem value="all">All Categories</SelectItem>
                            <SelectItem value="lifestyle">Lifestyle & Fashion</SelectItem>
                            <SelectItem value="tech">Tech Reviews</SelectItem>
                            <SelectItem value="fitness">Fitness & Wellness</SelectItem>
                            <SelectItem value="comedy">Comedy & Entertainment</SelectItem>
                          </SelectContent>
                        </Select>
                        <Select value={selectedPlatform} onValueChange={(value) => setSelectedPlatform(value)}>
                          <SelectTrigger className="border-gray-200 bg-white/80 backdrop-blur-sm focus:border-purple-300 focus:ring-purple-200">
                            <SelectValue placeholder="Platform" />
                          </SelectTrigger>
                          <SelectContent className="bg-white/95 backdrop-blur-sm border-gray-200">
                            <SelectItem value="all">All Platforms</SelectItem>
                            <SelectItem value="instagram">Instagram</SelectItem>
                            <SelectItem value="youtube">YouTube</SelectItem>
                            <SelectItem value="tiktok">TikTok</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="md:col-span-4 flex justify-end">
                        <Button
                          onClick={() => {
                            // Apply all filters at once
                            fetchInfluencers();
                          }}
                          variant="outline"
                          className="border-purple-200 hover:border-purple-300 hover:bg-purple-50"
                          disabled={isLoading}
                        >
                          Apply Filters
                        </Button>
                      </div>
                    </div>

                    {/* Results Count */}
                    <div className="mb-6">
                      {isLoading ? (
                        <p className="text-sm text-gray-600">
                          Searching for influencers...
                        </p>
                      ) : error ? (
                        <p className="text-sm text-red-600">
                          Error: {error}. Showing fallback data.
                        </p>
                      ) : (
                        <p className="text-sm text-gray-600">
                          {searchInputValue ? (
                            <>Found <span className="font-semibold text-purple-600">{filteredInfluencers.length}</span> influencers matching "{searchInputValue}"</>
                          ) : (
                            <>Showing <span className="font-semibold text-purple-600">{filteredInfluencers.length}</span> influencers</>
                          )}
                        </p>
                      )}
                    </div>

                    {/* Influencer Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                      {isLoading ? (
                        // Loading skeleton
                        Array(6).fill(0).map((_, index) => (
                          <Card key={`skeleton-${index}`} className="border border-gray-200/60 bg-white/80 backdrop-blur-sm shadow-sm h-[300px] animate-pulse">
                            <div className="p-4">
                              <div className="w-3/4 h-6 bg-gray-200 rounded mb-4"></div>
                              <div className="w-1/2 h-4 bg-gray-200 rounded mb-6"></div>
                              <div className="w-full h-24 bg-gray-200 rounded mb-4"></div>
                              <div className="flex justify-between">
                                <div className="w-1/3 h-8 bg-gray-200 rounded"></div>
                                <div className="w-1/3 h-8 bg-gray-200 rounded"></div>
                              </div>
                            </div>
                          </Card>
                        ))
                      ) : filteredInfluencers.length > 0 ? (
                        filteredInfluencers.map((influencer) => (
                          <InfluencerCard
                            key={influencer.id}
                            influencer={influencer}
                            onEmailOutreach={handleEmailOutreach}
                            onVoiceNegotiation={startVoiceNegotiation}
                          />
                        ))
                      ) : (
                        <div className="col-span-full text-center py-12">
                          <p className="text-gray-500">No influencers found matching your criteria. Try adjusting your search.</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Dashboard Tab */}
              <TabsContent value="dashboard" className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatsCard
                    title="Total Outreach"
                    value={outreachStats.totalOutreach}
                    change="+12% from last month"
                    icon={Mail}
                    trend="up"
                  />
                  <StatsCard
                    title="Response Rate"
                    value={`${Math.round((outreachStats.responses / outreachStats.totalOutreach) * 100)}%`}
                    change="+8% from last month"
                    icon={TrendingUp}
                    trend="up"
                  />
                  <StatsCard
                    title="Deals Closed"
                    value={outreachStats.deals}
                    change="+25% from last month"
                    icon={Star}
                    trend="up"
                  />
                  <StatsCard
                    title="Revenue Generated"
                    value={`$${outreachStats.revenue.toLocaleString()}`}
                    change="+30% from last month"
                    icon={DollarSign}
                    trend="up"
                  />
                </div>

                {/* Recent Activity */}
                <Card className="border border-gray-200/60 bg-white/80 backdrop-blur-sm shadow-sm">
                  <CardHeader>
                    <CardTitle className="text-xl">Recent Negotiations</CardTitle>
                    <CardDescription>Track your latest influencer outreach and negotiation results</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {mockInfluencers.slice(0, 3).map((influencer, index) => (
                        <div key={influencer.id} className="flex items-center justify-between p-4 border border-gray-200/60 rounded-xl bg-white/50 hover:bg-white/80 transition-all duration-200">
                          <div className="flex items-center space-x-4">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-medium">
                              {influencer.name.split(' ').map(n => n[0]).join('')}
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">{influencer.name}</p>
                              <p className="text-sm text-gray-500">{influencer.category}</p>
                            </div>
                          </div>
                          <div className="text-right flex items-center gap-3">
                            <Badge className={
                              index === 0 
                                ? "bg-green-100 text-green-800 border-green-200" 
                                : index === 1 
                                ? "bg-yellow-100 text-yellow-800 border-yellow-200" 
                                : "bg-blue-100 text-blue-800 border-blue-200"
                            }>
                              {index === 0 ? "Deal Closed" : index === 1 ? "Negotiating" : "Pending Response"}
                            </Badge>
                            <p className="text-sm font-medium text-gray-900">{influencer.pricing}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </main>
        </SidebarInset>

        {/* Email Outreach Dialog */}
        <Dialog open={emailDialogOpen} onOpenChange={setEmailDialogOpen}>
          <DialogContent className="sm:max-w-[525px] bg-white/95 backdrop-blur-xl border-gray-200/60">
            <DialogHeader>
              <DialogTitle className="text-xl">AI Email Outreach</DialogTitle>
              <DialogDescription className="text-gray-600">
                Our AI agent will craft and send a personalized outreach email to {selectedInfluencer?.name}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="p-4 bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl border border-purple-200/60">
                <h4 className="font-medium mb-2 text-gray-900">Generated Email Preview:</h4>
                <p className="text-sm text-gray-700 leading-relaxed">
                  Hi {selectedInfluencer?.name},<br/><br/>
                  I hope this message finds you well! I'm reaching out from [Brand Name] because we absolutely love your content in the {selectedInfluencer?.category} space. Your engagement rates and authentic connection with your audience align perfectly with our upcoming campaign.<br/><br/>
                  We'd love to discuss a potential collaboration opportunity. Would you be available for a brief call to explore this further? Please share your preferred contact number, and we can schedule something at your convenience.<br/><br/>
                  Looking forward to potentially working together!<br/><br/>
                  Best regards,<br/>
                  AI Marketing Agent
                </p>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setEmailDialogOpen(false)} className="border-gray-200">
                  Cancel
                </Button>
                <Button onClick={sendEmail} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white">
                  Send Email
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>

        {/* Voice Negotiation Dialog */}
        <Dialog open={voiceDialogOpen} onOpenChange={setVoiceDialogOpen}>
          <DialogContent className="sm:max-w-[525px] bg-white/95 backdrop-blur-xl border-gray-200/60">
            <DialogHeader>
              <DialogTitle className="text-xl">AI Voice Negotiation Setup</DialogTitle>
              <DialogDescription className="text-gray-600">
                Configure your campaign details for the AI voice agent to conduct negotiations with {selectedInfluencer?.name}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="brandName" className="text-sm font-medium text-gray-700">Brand Name</Label>
                  <Input
                    id="brandName"
                    placeholder="Your brand name"
                    value={campaignDetails.brandName}
                    onChange={(e) => setCampaignDetails({...campaignDetails, brandName: e.target.value})}
                    className="mt-1 border-gray-200 focus:border-purple-300 focus:ring-purple-200"
                  />
                </div>
                <div>
                  <Label htmlFor="campaignName" className="text-sm font-medium text-gray-700">Campaign Name</Label>
                  <Input
                    id="campaignName"
                    placeholder="Campaign title"
                    value={campaignDetails.campaignName}
                    onChange={(e) => setCampaignDetails({...campaignDetails, campaignName: e.target.value})}
                    className="mt-1 border-gray-200 focus:border-purple-300 focus:ring-purple-200"
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="deliverables" className="text-sm font-medium text-gray-700">Deliverables</Label>
                <Textarea
                  id="deliverables"
                  placeholder="1 Instagram post, 3 stories, 1 reel..."
                  value={campaignDetails.deliverables}
                  onChange={(e) => setCampaignDetails({...campaignDetails, deliverables: e.target.value})}
                  className="mt-1 border-gray-200 focus:border-purple-300 focus:ring-purple-200 resize-none"
                  rows={3}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="timeline" className="text-sm font-medium text-gray-700">Timeline</Label>
                  <Input
                    id="timeline"
                    placeholder="2 weeks"
                    value={campaignDetails.timeline}
                    onChange={(e) => setCampaignDetails({...campaignDetails, timeline: e.target.value})}
                    className="mt-1 border-gray-200 focus:border-purple-300 focus:ring-purple-200"
                  />
                </div>
                <div>
                  <Label htmlFor="budget" className="text-sm font-medium text-gray-700">Budget Range</Label>
                  <Input
                    id="budget"
                    placeholder="$2,000 - $4,000"
                    value={campaignDetails.budget}
                    onChange={(e) => setCampaignDetails({...campaignDetails, budget: e.target.value})}
                    className="mt-1 border-gray-200 focus:border-purple-300 focus:ring-purple-200"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-2 pt-4">
                <Button variant="outline" onClick={() => setVoiceDialogOpen(false)} className="border-gray-200">
                  Cancel
                </Button>
                <Button onClick={simulateVoiceCall} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white">
                  <Phone className="w-4 h-4 mr-2" />
                  Start Voice Negotiation
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </SidebarProvider>
  );
};

export default Index;
