import React from 'react';
import { shallow } from 'enzyme';

import UsersList from '../UsersList';

import renderer from 'react-test-renderer';

const users = [
    {
        'active': true,
        'email': 'brandux@upeu.edu.pe',
        'id': 1,
        'username': 'brandux'
    },
    {
        'active': true,
        'email': 'didier@upeu.edu.pe',
        'id': 2,
        'username': 'didier'
    },
]

test('UsersList rendering propely', () => {
    const wrapper = shallow(<UsersList users= {users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('brandux');
});

test('UsersList renders a snapshop propely', () => {
    const tree = renderer.create(<UsersList users = {users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});
