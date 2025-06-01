import React, { useState, useEffect } from 'react';
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";

interface Influencer {
  id: number;
  name: string;
  platforms: string[];
  category: string;
  followers: number;
  engagement_rate: number;
  region: string;
  rate_card: string;
  contact: string;
  description?: string;
}

const InfluencersPage: React.FC = () => {
  const [influencers, setInfluencers] = useState<Influencer[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all influencers on component mount
  useEffect(() => {
    fetchInfluencers();
  }, []);

  // Function to fetch all influencers
  const fetchInfluencers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/influencers/');
      if (!response.ok) {
        throw new Error('Failed to fetch influencers');
      }
      const data = await response.json();
      setInfluencers(data);
    } catch (err) {
      setError('Error fetching influencers. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Function to search influencers
  const searchInfluencers = async () => {
    if (!searchQuery.trim()) {
      fetchInfluencers();
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/influencers/search?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) {
        throw new Error('Failed to search influencers');
      }
      const data = await response.json();
      setInfluencers(data);
    } catch (err) {
      setError('Error searching influencers. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Format large numbers with commas
  const formatNumber = (num: number): string => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Influencer Discovery</h1>
      
      {/* Search bar */}
      <div className="flex gap-2 mb-8">
        <Input
          type="text"
          placeholder="Search influencers (e.g., 'beauty influencers in India with high engagement')"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1"
        />
        <Button onClick={searchInfluencers} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </Button>
        <Button variant="outline" onClick={fetchInfluencers} disabled={loading}>
          Reset
        </Button>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Influencer cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {influencers.map((influencer) => (
          <Card key={influencer.id} className="overflow-hidden">
            <CardHeader className="pb-2">
              <div className="flex justify-between items-start">
                <CardTitle>{influencer.name}</CardTitle>
                <Badge variant="outline" className="capitalize">
                  {influencer.category}
                </Badge>
              </div>
              <CardDescription>{influencer.region}</CardDescription>
            </CardHeader>
            <CardContent className="pb-2">
              <div className="space-y-2">
                <div className="flex flex-wrap gap-1">
                  {influencer.platforms.map((platform) => (
                    <Badge key={platform} variant="secondary">
                      {platform}
                    </Badge>
                  ))}
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="font-medium">Followers:</span>{' '}
                    {formatNumber(influencer.followers)}
                  </div>
                  <div>
                    <span className="font-medium">Engagement:</span>{' '}
                    {influencer.engagement_rate}%
                  </div>
                </div>
                <div className="text-sm">
                  <span className="font-medium">Rate Card:</span>{' '}
                  {influencer.rate_card}
                </div>
                {influencer.description && (
                  <div className="text-sm mt-2">
                    {influencer.description}
                  </div>
                )}
              </div>
            </CardContent>
            <CardFooter className="pt-2">
              <div className="text-sm text-gray-500">
                <span className="font-medium">Contact:</span>{' '}
                {influencer.contact}
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* No results message */}
      {!loading && influencers.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">No influencers found. Try a different search query.</p>
        </div>
      )}
    </div>
  );
};

export default InfluencersPage;
