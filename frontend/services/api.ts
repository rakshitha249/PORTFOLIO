export const fetchApi = async (endpoint: string) => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    const res = await fetch(`${apiUrl}${endpoint}`, {
      cache: 'no-store'
    });
    if (!res.ok) {
        if (res.status === 404) return null;
        throw new Error(`API responded with status ${res.status}`);
    }
    const data = await res.json();
    return data.results !== undefined ? data.results : data;
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return null;
  }
};

export const getProjects = () => fetchApi('/projects/').then(r => r || []);
export const getProjectBySlug = (slug: string) => fetchApi(`/projects/${slug}/`);
export const getProfile = () => fetchApi('/profile/').then(r => r || []);
export const getSkills = () => fetchApi('/skills/').then(r => r || []);
export const getExperience = () => fetchApi('/experience/').then(r => r || []);
export const getEducation = () => fetchApi('/education/').then(r => r || []);
export const getCertificates = () => fetchApi('/certificates/').then(r => r || []);
export const getSocialLinks = () => fetchApi('/social-links/').then(r => r || []);

export const getGithubRepositories = (params?: { language?: string, topic?: string, search?: string, sort?: string, limit?: number }) => {
  let url = '/github/repositories/';
  if (params) {
    const searchParams = new URLSearchParams();
    if (params.language) searchParams.append('language', params.language);
    if (params.topic) searchParams.append('topic', params.topic);
    if (params.search) searchParams.append('search', params.search);
    if (params.sort) searchParams.append('sort', params.sort);
    if (params.limit) searchParams.append('limit', params.limit.toString());
    const queryString = searchParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
  }
  return fetchApi(url).then(r => r || []);
};
